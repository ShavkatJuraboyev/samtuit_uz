from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.text import slugify
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now

class Menu(models.Model):
    title_uz = models.CharField(max_length=100, verbose_name='Uzbek tilida menu')
    title_ru = models.CharField(max_length=100, verbose_name='Rus tilida menu')
    title_en = models.CharField(max_length=100, verbose_name='Ingliz tilida menu')
    url = models.CharField(max_length=200, blank=True, null=True, default="http://127.0.0.1:8000/")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name="Ota menyu" )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    class Meta:
        verbose_name = "Menyu" 
        verbose_name_plural = "Menyular" 


    def __str__(self):
        return self.title_uz
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_menu_title(self, language):
        return self.get_translation('title', language) 

class ListsMenu(models.Model):
    title_uz = models.CharField(max_length=100, verbose_name='Uzbek tilida menu')
    title_en = models.CharField(max_length=100, verbose_name='Engliz tilida menu')
    title_ru = models.CharField(max_length=100, verbose_name='Rus tilida menu')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name="Ota menyu" )
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug", help_text="Ushbu urlni tanlangan Menu saxifasidagi urlga joylashtiring")
    url = models.CharField(max_length=200, blank=True, null=True, default=f"http://127.0.0.1:8000/")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_lists_title(self, language):
        return self.get_translation('title', language)
    
    class Meta:
        verbose_name = "Menyular"
    
    @property
    def translated_title(self):
        from django.utils.translation import get_language
        language = get_language()  # Joriy tilni aniqlash
        return self.get_lists_title(language)

class Lists(models.Model):
    listmenu = models.ForeignKey(ListsMenu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menusi", help_text="Menuyuda aks etadi")
    url = models.CharField(max_length=255, null=True, blank=True, help_text="Boshqa web saytga yonaltirish", verbose_name="Url")
    files = models.FileField(upload_to="files", null=True, blank=True, help_text="Fayl yuklash agar kerak bo'lsa", verbose_name="Fayl")

    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = RichTextUploadingField(config_name='extends_uz', blank=True, verbose_name="Sarlovha umumiy matini")

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, blank=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = RichTextUploadingField(config_name='extends_en', blank=True, verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = RichTextUploadingField(config_name='extends_ru', blank=True, verbose_name="Ruscha sarlovha umumiy matini", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Qoshimcha ma'lumotlar"
     
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_list_title(self, language):
        return self.get_translation('title', language)

    def get_list_text(self, language):
        return self.get_translation('text', language)

    def get_list_content(self, language):
        return self.get_translation('content', language)
    
    def __str__(self):
        return self.title_uz

class PictureSlider(models.Model):
    image = models.ImageField(upload_to="silder/", help_text="Silayder rasmlari yuklash uchun")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

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
    title_uz = models.CharField(max_length=250, null=True, blank=True, verbose_name="Savollar", help_text="O'zbek tilida yozing. Maksimal 250 belgi")
    text_uz = models.CharField(max_length=600, null=True, blank=True, verbose_name="Javoblar", help_text="O'zbek tilida yozing. Maksimal 600 belgi")

    title_en = models.CharField(max_length=250, null=True, blank=True, verbose_name="Savollar", help_text="Engliz tilida yozing. Maksimal 250 belgi")
    text_en = models.CharField(max_length=600, null=True, blank=True, verbose_name="Javoblar", help_text="Engliz tilida yozing. Maksimal 600 belgi")

    title_ru = models.CharField(max_length=250, null=True, blank=True, verbose_name="Savollar", help_text="Rus tilida yozing. Maksimal 250 belgi")
    text_ru = models.CharField(max_length=600, null=True, blank=True, verbose_name="Javoblar", help_text="Rus tilida yozing. Maksimal 600 belgi")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Savollar va javoblar"

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
      
class Season(models.Model):
    season = models.CharField(default="Fasllar", max_length=50)
    snow = models.BooleanField()
    leaf = models.BooleanField()
    rain = models.BooleanField()
    spring = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.season

class QuickMmenu(models.Model):
    title_uz = models.CharField(max_length=100, verbose_name='Uzbek tilida menu')
    title_ru = models.CharField(max_length=100, verbose_name='Rus tilida menu')
    title_en = models.CharField(max_length=100, verbose_name='Ingliz tilida menu')
    url = models.CharField(max_length=200, blank=True, null=True, default="http://127.0.0.1:8000/")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    class Meta:
        verbose_name = "Tezkor Menyu" 
        verbose_name_plural = "Tezkor Menyular" 


    def __str__(self):
        return self.title_uz
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_menu_title(self, language):
        return self.get_translation('title', language) 