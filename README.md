# PlantAI – AI Destekli Bitki Hastalık Teşhisi ve İlaç Öneri Sistemi

## 1. Proje Tanımı
PlantAI, kullanıcıların bitki hastalıklarını yapay zeka yardımıyla tespit edip, tespit edilen hastalığa uygun bitki ilaçlarını satın alabilecekleri bir e-ticaret platformudur.  
Sistem, kullanıcıların yüklediği bitki fotoğraflarını analiz ederek hastalık tespiti yapar ve bu hastalık için veritabanında kayıtlı ilaç önerilerini listeler.  

Tüm işlem süreci **asenkron** olarak çalışır. Yani kullanıcı, tahmin işlemleri tamamlanana kadar sistemde diğer sayfalarda gezinebilir veya yeni işlemler başlatabilir.  
Bu yapı sayesinde, yüksek boyutlu görsellerin işlenmesi veya model tahmin sürelerinin kullanıcı deneyimini olumsuz etkilemesi önlenmiş olur.

---
## Demo

<p align="center">
  <img src="PlantAI/media/gif/Analiz.gif" width="800"><br>
  <b>Analiz Sayfası</b>
</p>

<p align="center">
  <img src="PlantAI/PlantAI/media/gif/Home.gif" width="800"><br>
  <b>Ana Sayfa</b>
</p>

<p align="center">
  <img src="PlantAI/media/gif/Urunler.gif" width="800"><br>
  <b>Ürünler Sayfası</b>
</p>
## 2. Mimari Yapı
Proje üç ana bileşenden oluşmaktadır:

- **Backend:** Django REST Framework (DRF) ile API geliştirme, veritabanı yönetimi, iş mantığının yazılması ve Celery üzerinden uzun süren yapay zeka işlemlerinin yönetimi.
- **Frontend:** Vue.js ile modern, hızlı ve kullanıcı dostu bir arayüz. API ile etkileşim kurarak kullanıcıya tahmin sonuçlarını ve ilaç önerilerini sunar.
- **Mesaj Kuyruğu:** RabbitMQ, arka plan görevlerinin (model çalıştırma, veri işleme vb.) yönetimi için kullanılır. Yüksek yoğunlukta gelen işlemler bu sistem sayesinde sıraya alınır ve güvenli şekilde işlenir.

Bu mimari, hem ölçeklenebilir hem de bakım yapılabilir bir sistem oluşturmak için tercih edilmiştir.

---

## 3. Yapay Zeka Modeli Hakkında Bilgiler
Bu projede kullanılan yapay zeka modeli, derin öğrenme tabanlı bir görüntü sınıflandırma sistemidir. Tarımsal bitki yaprağı görüntülerinden hastalık teşhisi yapmak üzere eğitilmiştir.

**Model Özellikleri:**
- **Toplam kapsama:** 14 bitki türü, 38 farklı hastalık sınıfı (sağlıklı yapraklar dahil)
- **Veri seti:** “New Plant Diseases Dataset” — hem sağlıklı hem de hastalıklı yaprak görüntülerini içerir
- **Mimari:** CNN tabanlı, PyTorch ile geliştirilmiş; ayrıca VGG16 ve ResNet34 gibi transfer öğrenme yöntemleriyle denemeler yapılmıştır
- **Başarı oranı:** Test doğruluğu en iyi modelde **%98.42** olarak ölçülmüştür
- **Çıkış formatı:** Hastalık sınıfı ve olasılık yüzdesi (örn: *Tomato – Early Blight %97.8*)

**Kapsadığı bitkiler ve hastalıklar:**
Apple: Apple Scab, Black Rot, Cedar Apple Rust, Healthy  
Blueberry: Healthy  
Cherry: Powdery Mildew, Healthy  
Corn: Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy  
Grape: Black Rot, Esca, Leaf Blight, Healthy  
Orange: Huanglongbing (Citrus Greening)  
Peach: Bacterial Spot  
Pepper: Bacterial Spot, Healthy  
Potato: Early Blight, Late Blight, Healthy  
Raspberry: Healthy  
Soybean: Healthy  
Squash: Powdery Mildew  
Strawberry: Leaf Scorch, Healthy  
Tomato: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus, Healthy

Model, yüklenen yaprak fotoğrafını analiz ederek bu 38 sınıftan birine ait olduğunu belirler. Ardından sistem, bu sınıfa ait hastalık bilgilerini **DiseaseInfo** tablosundan, uygun ilaç bilgilerini ise **Pesticide** tablosundan çeker.

---

## 4. Veritabanı Yapısı
Sistemde dört temel tablo bulunmaktadır:

1. **Workflow:** Yüklenen görsellerin işlenme süreci ve genel durum bilgisini tutar. *(pending, uploaded, preprocessed, predicted, completed, failed)*
2. **WorkflowStep:** Workflow içindeki her adımın (yükleme, ön işleme, tahmin) detaylı kaydı. Böylece hangi adımda hata oluştuğu veya ne zaman tamamlandığı takip edilebilir.
3. **Pesticide:** İlgili hastalıklar için önerilen bitki ilaçlarının bilgilerini içerir. İlaç adı, fiyatı, ağırlığı, stok durumu ve görseli bu tabloda saklanır.
4. **DiseaseInfo:** Hastalıkların tanımı, belirtileri ve genel açıklamalarını içerir. Böylece kullanıcıya yalnızca ilaç değil, hastalık hakkında da bilgilendirme yapılabilir.

---

## 5. Projeyi Çalıştırma

**Backend – Django geliştirme sunucusu başlatma:**
```bash
python manage.py runserver
