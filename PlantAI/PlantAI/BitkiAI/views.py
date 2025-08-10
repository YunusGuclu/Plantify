from django.shortcuts import render
from django.http import JsonResponse
from .models import Workflow, Pesticide, DiseaseInfo
from .utils import run_workflow
from celery.result import AsyncResult
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404

def home(request):
    """
    Anasayfa: yükleme formunu gösterir.
    """
    return render(request, 'home.html')

def start_workflow(request):
    """
    POST ile gelen resmi alır, yeni bir Workflow yaratır,
    celery zincirini başlatır ve task_id döner.
    """
    if request.method == 'POST' and request.FILES.get('image'):
        workflow   = Workflow.objects.create(name='Bitki Hastalık Tespiti')
        image_file = request.FILES['image']
        file_bytes = image_file.read()
        filename   = image_file.name
        task_id    = run_workflow(file_bytes, filename, workflow.id)
        return JsonResponse({'task_id': task_id})
    return render(request, 'home.html')

def task_status(request):
    """
    GET?task_id=... ile çağrıldığında task durumu, sonucu ve
    tahmin edilen sınıfa (class_name) göre ilaç önerilerini ve
    hastalık açıklamasını döner.
    """
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'error': 'task_id eksik'}, status=400)

    async_res = AsyncResult(task_id)
    data      = {'state': async_res.state}

    if async_res.ready():
        payload = async_res.get()
        data.update(payload)

        # payload['label'] = sınıf kodu, örn. 'Pepper,_bell___Bacterial_spot'
        cls_code = payload.get('label')

        # Hastalık bilgisi çek
        try:
            di = DiseaseInfo.objects.get(class_name=cls_code)
            data['disease_info'] = {
                'disease':     di.disease,
                'description': di.description,
            }
        except DiseaseInfo.DoesNotExist:
            data['disease_info'] = None

        # Önerilen ilaçları çek
        recs = Pesticide.objects.filter(
            class_name=cls_code,
            is_active=True
        )
        data['pesticides'] = [
            {
                'name':        p.name,
                'image':       request.build_absolute_uri(p.image.url) if p.image else None,
                'weight_gram': float(p.weight_gram),
                'price':       float(p.price),
                'description': p.description,
            }
            for p in recs
        ]

    return JsonResponse(data)

def products(request):
    """
    Return JSON with:
      - popular: en çok satan (sales_count desc)
      - new: en son eklenen (created_at desc)
    """
    popular_qs = Pesticide.objects.filter(is_active=True).order_by('-sales_count')[:4]
    new_qs     = Pesticide.objects.filter(is_active=True).order_by('-created_at')[:4]

    def serialize(qs):
        return [
            {
                'id':           p.id,
                'name':         p.name,
                'image':        request.build_absolute_uri(p.image.url) if p.image else None,
                'price':        float(p.price),
                'weight_gram':  float(p.weight_gram),
                'description':  p.description,
            }
            for p in qs
        ]

    return JsonResponse({
        'popular': serialize(popular_qs),
        'new':     serialize(new_qs),
    })

@require_GET
def all_products(request):
    """
    GET ile yayında (is_active=True) olan tüm ilaçları döner.
    ?sort=price  → fiyat düşükten yükseğe
    ?sort=sales  → en çok satanlar (sales_count yüksekten düşüğe)
    """
    sort = request.GET.get('sort', 'price')
    qs = Pesticide.objects.filter(is_active=True)

    if sort == 'sales':
        qs = qs.order_by('-sales_count')
    else:
        qs = qs.order_by('price')

    products_list = [
        {
            'id':          p.id,
            'name':        p.name,
            'image':       request.build_absolute_uri(p.image.url) if p.image else None,
            'price':       float(p.price),
            'weight_gram': float(p.weight_gram),
            'description': p.description,
            'disease':     p.disease,
            'class_name':  p.class_name,
        }
        for p in qs
    ]

    return JsonResponse({'products': products_list})

@require_GET
def product_detail(request, name):
    """
    Ürün detay sayfası: verilen name ile Bitki İlacı'nın tüm
    alanlarını JSON olarak döner.
    """
    p = get_object_or_404(Pesticide, name=name, is_active=True)
    data = {
        'id':           p.id,
        'class_name':   p.class_name,
        'disease':      p.disease,
        'name':         p.name,
        'image':        request.build_absolute_uri(p.image.url) if p.image else None,
        'weight_gram':  float(p.weight_gram),
        'description':  p.description,
        'price':        float(p.price),
        'stock':        p.stock,
    }
    return JsonResponse({'product': data})