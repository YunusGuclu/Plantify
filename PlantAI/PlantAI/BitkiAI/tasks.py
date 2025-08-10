# BitkiAI/tasks.py

import os
import tempfile
from pathlib import Path
from celery import shared_task
from PIL import Image
import torch
from torch import nn
from torchvision import transforms, models
from .models import WorkflowStep, Workflow

# Model dosyasının yolu
BASE_DIR   = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, 'BitkiAI', 'model', 'plantDisease-resnet34.pth')

# Sınıf isimleri
CLASS_NAMES = [
    'Apple___Apple_scab','Apple___Black_rot','Apple___Cedar_apple_rust','Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew','Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot','Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy',
    'Grape___Black_rot','Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot','Peach___healthy',
    'Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy',
    'Potato___Early_blight','Potato___Late_blight','Potato___healthy',
    'Raspberry___healthy','Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch','Strawberry___healthy',
    'Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight',
    'Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy'
]

# Cihaz seçimi
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model tanımı
class PlantDiseaseResNet34(nn.Module):
    def __init__(self, num_classes: int):
        super().__init__()
        self.network = models.resnet34(pretrained=False)
        in_feats     = self.network.fc.in_features
        self.network.fc = nn.Linear(in_feats, num_classes)

    def forward(self, x):
        return self.network(x)

MODEL = None
def get_model():
    global MODEL
    if MODEL is None:
        state     = torch.load(MODEL_PATH, map_location=device)
        out_feats = state['network.fc.weight'].size(0)
        MODEL     = PlantDiseaseResNet34(num_classes=out_feats)
        MODEL.load_state_dict(state)
        MODEL.to(device).eval()
    return MODEL

# 1) Görseli al, tmp dosyaya kaydet, adımı tamamla
@shared_task(bind=True)
def upload_image(self, file_bytes: bytes, filename: str,
                 upload_step: int, preprocess_step: int,
                 predict_step: int, save_step: int):
    step     = WorkflowStep.objects.get(pk=upload_step)
    workflow = step.workflow
    workflow.status = 'uploaded'
    workflow.save()
    step.status = 'completed'
    step.save()

    # OS geçici dizininde resmi kaydet
    suffix  = os.path.splitext(filename)[1] or '.jpg'
    tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_img.write(file_bytes)
    tmp_img.flush()
    tmp_img.close()

    return {
        'tmp_image_path':  tmp_img.name,
        'preprocess_step': preprocess_step,
        'predict_step':    predict_step,
        'save_step':       save_step
    }

# 2) Geçici resim dosyasını işle, tmp tensor dosyası oluştur
@shared_task(bind=True)
def preprocess_image(self, data: dict):
    step     = WorkflowStep.objects.get(pk=data['preprocess_step'])
    workflow = step.workflow
    workflow.status = 'preprocessed'
    workflow.save()

    # Temp resimden oku
    img = Image.open(data['tmp_image_path']).convert('RGB')
    tf = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])
    tensor = tf(img)

    # Tensor’ı temp dosyaya yaz
    tmp_tensor = tempfile.NamedTemporaryFile(delete=False, suffix='.pt')
    torch.save(tensor, tmp_tensor.name)
    tmp_tensor.close()

    step.status = 'completed'
    step.save()
    return {
        'tmp_image_path':  data['tmp_image_path'],
        'tmp_tensor_path': tmp_tensor.name,
        'predict_step':    data['predict_step'],
        'save_step':       data['save_step']
    }

# 3) Tensor’ı yükle, model ile tahmin et
@shared_task(bind=True)
def predict_image(self, data: dict):
    step     = WorkflowStep.objects.get(pk=data['predict_step'])
    workflow = step.workflow
    workflow.status = 'predicted'
    workflow.save()

    tensor = torch.load(data['tmp_tensor_path'])
    tensor = tensor.unsqueeze(0).to(device)
    model  = get_model()
    with torch.no_grad():
        out, pred = model(tensor), None
        _, pred  = torch.max(out,1)

    idx   = pred.item()
    label = CLASS_NAMES[idx] if 0 <= idx < len(CLASS_NAMES) else f"Unknown({idx})"

    step.status = 'completed'
    step.result = label
    step.save()
    return {
        'label':           label,
        'save_step':       data['save_step'],
        'tmp_image_path':  data['tmp_image_path'],
        'tmp_tensor_path': data['tmp_tensor_path']
    }

# 4) Sonuçları kaydet, workflow’u güncelle, temp dosyaları sil
@shared_task(bind=True)
def save_result(self, data: dict):
    step     = WorkflowStep.objects.get(pk=data['save_step'])
    workflow = step.workflow
    workflow.status  = 'completed'
    workflow.result  = data['label']
    workflow.classes = ','.join(CLASS_NAMES)
    workflow.save()

    step.status  = 'completed'
    step.result  = data['label']
    step.classes = ','.join(CLASS_NAMES)
    step.save()

    # Ara dosyaları sil
    for path in (data.get('tmp_image_path'), data.get('tmp_tensor_path')):
        try:
            os.remove(path)
        except OSError:
            pass

    return {
        'label':       data['label'],
        'all_classes': CLASS_NAMES
    }
