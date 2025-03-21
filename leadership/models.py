from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField 
from django.templatetags.static import static
from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import now

# Create your models here.

class Leadership(models.Model):
    POSITION = [
        ('rektor', 'Rektor'),
        ('o\'rinbosar', 'O\'rinbosar')
    ]
    full_name_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", verbose_name="To'liq F.I.O Uzb:")
    full_name_en = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Englizcha kiriting", verbose_name="To'liq F.I.O Eng:")
    full_name_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Ruscha kiriting", verbose_name="To'liq F.I.O Rus:")
    image = models.ImageField(upload_to='rektorat/', null=True, blank=True, verbose_name="Direktor rasmi", help_text="Rasm o‘lchami 270x201 piksel bo‘lishi kerak!")
    acceptance = models.CharField(max_length=100, null=True, blank=True, help_text="Chorshanba - Juma, 15:00 - 17:00", verbose_name="Qabul:")
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="+998901234567", verbose_name="Telefon:")
    email = models.CharField(max_length=200, null=True, blank=True, help_text="z.karshiyev@samtuit.uz, zaynidin85@gmail.com", verbose_name="Email:")
    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Biografiya Uzb", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Biografiya Eng", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Biografiya Rus", null=True, blank=True)
    positions = models.CharField(max_length=20, choices=POSITION, verbose_name="Lavozim nomi:")
    position_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Uzb nomi:")
    position_en = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Eng nomi:")
    position_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Rus nomi:")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Rektorat"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_rek_full_name(self, language):
        return self.get_translation('full_name', language)

    def get_rek_content(self, language):
        return self.get_translation('content', language)
    
    def get_rek_position(self, language):
        return self.get_translation('position', language)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name_en)
        super().save(*args, **kwargs)
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Leadership.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Leadership.DoesNotExist:
            pass
        super(Leadership, self).save(*args, **kwargs)

    def get_rek_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('users/images/person-240x300.png')

        
    def __str__(self):
        return self.full_name_uz

class Faculty(models.Model):
    image = models.ImageField(upload_to='kafedra/', null=True, blank=True, verbose_name="Kafedra rasmi", help_text="Rasm o‘lchami 740x500 piksel bo‘lishi kerak!")
    title_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi O'zbekcha kiriting", verbose_name="Kafedra nomi UZB")
    title_en = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi Englizcha kiriting", verbose_name="Kafedra nomi ENG")
    title_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi Ruscha kiriting", verbose_name="Kafedra nomi RUS")

    text_uz = models.TextField(null=True, blank=True, help_text="Sarlovha", verbose_name="Sarlovha matini:")
    text_en = models.TextField(null=True, blank=True, help_text="Sarlovha", verbose_name="Sarlovha matini:")
    text_ru = models.TextField(null=True, blank=True, help_text="Sarlovha", verbose_name="Sarlovha matini:")
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Fakultetlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_facul_titul(self, language):
        return self.get_translation('title', language)
    
    def get_facul_text(self, language):
        return self.get_translation('text', language)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Faculty.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Faculty.DoesNotExist:
            pass
        super(Faculty, self).save(*args, **kwargs)

    def get_facul_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('users/images/person-240x300.png')

        
    def __str__(self):
        return self.title_uz

class FacultyDean(models.Model):
    POSITION = [
        ('dekan', 'Dekan'),
        ('o\'rinbosar', 'O\'rinbosar')
    ]
    full_name_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", verbose_name="To'liq F.I.O Uzb:")
    full_name_en = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Englizcha kiriting", verbose_name="To'liq F.I.O Eng:")
    full_name_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Ruscha kiriting", verbose_name="To'liq F.I.O Rus:")
    image = models.ImageField(upload_to='rektorat/', null=True, blank=True, verbose_name="Dekan rasmi", help_text="Rasm o‘lchami 270x201 piksel bo‘lishi kerak!")
    acceptance = models.CharField(max_length=100, null=True, blank=True, help_text="Chorshanba - Juma, 15:00 - 17:00", verbose_name="Qabul:")
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="+998901234567", verbose_name="Telefon:")
    email = models.CharField(max_length=200, null=True, blank=True, help_text="z.karshiyev@samtuit.uz, zaynidin85@gmail.com", verbose_name="Email:")
    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Biografiya Uzb", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Biografiya Eng", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Biografiya Rus", null=True, blank=True)
    positions = models.CharField(max_length=20, choices=POSITION, verbose_name="Lavozim nomi:")
    position_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Uzb nomi:")
    position_en = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Eng nomi:")
    position_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Lavozimini yozing", verbose_name="Lavozim Rus nomi:")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fakultet:", related_name='dekanlar')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Dekanat"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_dekan_full_name(self, language):
        return self.get_translation('full_name', language)

    def get_dekan_content(self, language):
        return self.get_translation('content', language)
    
    def get_dekan_position(self, language):
        return self.get_translation('position', language)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name_en)
        super().save(*args, **kwargs)
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = FacultyDean.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except FacultyDean.DoesNotExist:
            pass
        super(FacultyDean, self).save(*args, **kwargs)

    def get_dekan_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('users/images/person-240x300.png')

        
    def __str__(self):
        return self.full_name_uz

class Departments(models.Model):
    image = models.ImageField(upload_to='kafedra/', null=True, blank=True, verbose_name="Kafedra rasmi", help_text="Rasm o‘lchami 370x250 piksel bo‘lishi kerak!")
    titul_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi O'zbekcha kiriting", verbose_name="Kafedra nomi UZB")
    titul_en = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi Englizcha kiriting", verbose_name="Kafedra nomi ENG")
    titul_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi Ruscha kiriting", verbose_name="Kafedra nomi RUS")

    text_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_en = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    
    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Kafedra ma'limot Uzb", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Kafedra ma'limot Eng", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Kafedra ma'limot Rus", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fakultet:", related_name='kafedra') 

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Kafedralar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_dep_titul(self, language):
        return self.get_translation('titul', language)

    def get_dep_content(self, language):
        return self.get_translation('content', language) 
    
    def get_dep_text(self, language):
        return self.get_translation('text', language)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titul_en)
        super().save(*args, **kwargs)
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Departments.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Departments.DoesNotExist:
            pass
        super(Departments, self).save(*args, **kwargs)

    def get_dep_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('users/images/person-240x300.png')

        
    def __str__(self):
        return self.titul_uz 

class DepartmentsCenter(models.Model):
    image = models.ImageField(upload_to='kafedra/', null=True, blank=True, verbose_name="Bo'lim va markazlar rasmi", help_text="Rasm o‘lchami 370x250 piksel bo‘lishi kerak!")
    title_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Bo'lim va markazlar nomi O'zbekcha kiriting", verbose_name="Bo'lim va markazlar nomi UZB")
    title_en = models.CharField(max_length=200, null=True, blank=True, help_text="Bo'lim va markazlar nomi Englizcha kiriting", verbose_name="Bo'lim va markazlar nomi ENG")
    title_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Bo'lim va markazlar nomi Ruscha kiriting", verbose_name="Bo'lim va markazlar nomi RUS")

    text_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_en = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    
    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Bo'lim va markazlar ma'limot Uzb", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Bo'lim va markazlar ma'limot Eng", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Bo'lim va markazlar ma'limot Rus", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Bo'lim va markazlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_depcen_title(self, language):
        return self.get_translation('title', language)

    def get_depcen_content(self, language):
        return self.get_translation('content', language) 
    
    def get_depcen_text(self, language):
        return self.get_translation('text', language)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = DepartmentsCenter.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except DepartmentsCenter.DoesNotExist:
            pass
        super(DepartmentsCenter, self).save(*args, **kwargs)

    def get_dep_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('users/images/person-240x300.png')


        
    def __str__(self):
        return self.title_uz

 