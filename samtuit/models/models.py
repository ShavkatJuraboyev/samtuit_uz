from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.templatetags.static import static

class Menu(models.Model):
    title_uz = models.CharField(max_length=255, verbose_name='Uzbek tilida sarlavha')
    title_ru = models.CharField(max_length=255, verbose_name='Rus tilida sarlavha')
    title_en = models.CharField(max_length=255, verbose_name='Ingliz tilida sarlavha')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_uz  # Bu erda siz o'zingiz xohlagan tilni ko'rsatishingiz mumkin

    class Meta:
        verbose_name = 'Menu'
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
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
   