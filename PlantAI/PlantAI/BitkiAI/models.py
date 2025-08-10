from django.db import models

class Workflow(models.Model):
    name        = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    image       = models.ImageField("Görsel", upload_to="workflows/", null=True, blank=True)
    status      = models.CharField(
        "Genel Durum",
        max_length=20,
        default="pending",
        help_text="pending | uploaded | preprocessed | predicted | completed | failed"
    )
    result      = models.CharField(
        "Sonuç",
        max_length=100,
        null=True,
        blank=True
    )
    classes     = models.TextField(
        "Tüm Sınıflar",
        null=True,
        blank=True,
        help_text="Virgülle ayrılmış sınıf isimleri"
    )

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow   = models.ForeignKey(
        Workflow,
        related_name='steps',
        on_delete=models.CASCADE
    )
    name       = models.CharField(max_length=100)
    task_name  = models.CharField(max_length=200)
    order      = models.PositiveIntegerField()

    status     = models.CharField(
        max_length=20,
        default='pending',
        help_text="pending | started | completed | failed"
    )
    result     = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Bu adımın tahmin sonucu"
    )
    classes    = models.TextField(
        null=True,
        blank=True,
        help_text="Bu adımda kullanılan sınıflar"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['workflow', 'order']

    def __str__(self):
        return f"{self.workflow.name} – {self.name}"


class Pesticide(models.Model):
    class_name   = models.CharField("Sınıf Kodu", max_length=100)
    disease      = models.CharField("Hastalık Adı", max_length=200)
    name         = models.CharField("İlaç Adı", max_length=200)
    image        = models.ImageField("Görsel", upload_to="pesticides/", null=True, blank=True)
    weight_gram  = models.DecimalField("Ağırlık (g)", max_digits=8, decimal_places=2)
    description  = models.TextField("Açıklama", blank=True)
    price        = models.DecimalField("Fiyat (₺)", max_digits=10, decimal_places=2)
    stock        = models.PositiveIntegerField("Stok Adedi", default=0)
    sales_count  = models.PositiveIntegerField("Satış Adedi", default=0)
    is_active    = models.BooleanField("Yayında", default=True)
    created_at   = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bitki İlacı"
        verbose_name_plural = "Bitki İlaçları"

    def __str__(self):
        return f"{self.disease} → {self.name}"

class DiseaseInfo(models.Model):
    class_name = models.CharField("Sınıf Kodu", max_length=100, unique=True)
    disease    = models.CharField("Hastalık Adı", max_length=200)
    description = models.TextField("Açıklama", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['disease']
        verbose_name = "Hastalık Bilgisi"
        verbose_name_plural = "Hastalık Bilgileri"

    def __str__(self):
        return f"{self.disease} ({self.class_name})"