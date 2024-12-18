from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Menu(models.Model):
    MENU_TYPE_CHOICES = (
        ('list', 'List'),
        ('detail', 'Detail'),
    )
    title_uz = models.CharField(max_length=100, verbose_name='Uzbek tilida menu')
    title_ru = models.CharField(max_length=100, verbose_name='Rus tilida menu')
    title_en = models.CharField(max_length=100, verbose_name='Ingliz tilida menu')
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    menu_type = models.CharField(max_length=10, choices=MENU_TYPE_CHOICES, verbose_name="Menyu turi")
    linked_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bog'liq model")
    linked_object = models.PositiveIntegerField(blank=True, null=True, verbose_name="Bog'liq obyekt ID")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='children', 
        verbose_name="Ota menyu"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    def get_linked_model_instance(self):
        if self.linked_model and self.linked_object:
            model = apps.get_model(app_label='news', model_name=self.linked_model)
            return model.objects.filter(pk=self.linked_object).first()
        return None

    class Meta:
        verbose_name = "Menyu"
        verbose_name_plural = "Menyular"
        ordering = ['parent__id', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uz)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_menu_title(self, language):
        return self.get_translation('title', language)


class PictureSlider(models.Model):
    image = models.ImageField(upload_to="silder/", help_text="Silayder rasmlari yuklash uchun")

    class Meta:
        verbose_name_plural = "Rasm Slayderlari"

    def __str__(self):
        return f"{self.id}-rasm"
    
    def get_silder_img(self):
        return self.image.url if self.image else static('')
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = PictureSlider.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except PictureSlider.DoesNotExist:
            pass
        super(PictureSlider, self).save(*args, **kwargs)


class Partners(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Hamkor nomi")
    link = models.CharField(max_length=500, null=True, blank=True, verbose_name="Hamkor web sayt linki")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Hamkor rasmi .png")

    def get_hamk_img(self):
        return self.image.url if self.image else static('')

    class Meta:
        verbose_name_plural = "Hamkorlar"


class Students(models.Model): 
    frist_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    student_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    candidate = models.CharField(max_length=250, null=True, blank=True)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Talabalar"

    def get_student_img(self):
        return self.student_image.url if self.student_image else static('')
    
    def __str__(self):
        return f"{self.frist_name}-{self.last_name}"
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Students.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.student_image and this.student_image != self.student_image:
                this.student_image.delete(save=False)
        except Students.DoesNotExist:
            pass
        super(Students, self).save(*args, **kwargs)
   

class Wisdom(models.Model):
    title_uz = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="O'zbek tilida yozing. Maksimal 250 belgi")
    text_uz = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="O'zbek tilida yozing. Maksimal 500 belgi")

    title_en = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="Engliz tilida yozing. Maksimal 250 belgi")
    text_en = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="Engliz tilida yozing. Maksimal 500 belgi")

    title_ru = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="Rus tilida yozing. Maksimal 250 belgi")
    text_ru = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="Rus tilida yozing. Maksimal 500 belgi")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Kun hikmatlari"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_wis_title(self, language):
        return self.get_translation('title', language)

    def get_wis_text(self, language):
        return self.get_translation('text', language)
    
    def __str__(self):
        return self.title_uz

class Celebrities(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Muallif rasmi", help_text="Rasm o‘lchami 100x100 piksel bo‘lishi kerak!")
    title_uz = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="O'zbek tilida yozing. Maksimal 250 belgi")
    text_uz = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="O'zbek tilida yozing. Maksimal 500 belgi")

    title_en = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="Engliz tilida yozing. Maksimal 250 belgi")
    text_en = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="Engliz tilida yozing. Maksimal 500 belgi")

    title_ru = models.CharField(max_length=250, null=True, blank=True, verbose_name="Muallif ismi", help_text="Rus tilida yozing. Maksimal 250 belgi")
    text_ru = models.CharField(max_length=600, null=True, blank=True, verbose_name="Muallif so'zi", help_text="Rus tilida yozing. Maksimal 500 belgi")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Mashur so'zlar"

    def get_cel_img(self):
        return self.image.url if self.image else static('')

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_cel_title(self, language):
        return self.get_translation('title', language)

    def get_cel_text(self, language):
        return self.get_translation('text', language)

    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Celebrities.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Celebrities.DoesNotExist:
            pass
        super(Celebrities, self).save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Yuklangan rasmni ochish
        img = Image.open(self.image)

        # O'lchamni tekshirish
        if img.height > 100 or img.width > 100:
            raise ValidationError("Rasm o‘lchami 100x100 piksel bo‘lishi kerak!")