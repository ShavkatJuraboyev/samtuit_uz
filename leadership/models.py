from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField 
from django.templatetags.static import static
from django.utils.text import slugify

# Create your models here.

class Leadership(models.Model):
    POSITION = [
        ('rektor', 'Rektor'),
        ('o\'rinbosar', 'O\'rinbosar')
    ]
    full_name_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", verbose_name="To'liq F.I.O:")
    full_name_en = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Englizcha kiriting", verbose_name="To'liq F.I.O:")
    full_name_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Ruscha kiriting", verbose_name="To'liq F.I.O:")
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

    def clean(self):
        if not self.image:
            return  # Agar rasm yuklanmagan bo'lsa, to'xtaydi

        # Super class clean metodini chaqirish
        super().clean()

        try:
            # Yuklangan rasmni ochish
            img = Image.open(self.image)

            # O'lchamni tekshirish
            if img.height > 201 or img.width > 270:
                raise ValidationError("Rasm o‘lchami 270x201 piksel bo‘lishi kerak!")
        except Exception as e:
            raise ValidationError(f"Yuklangan rasm noto'g'ri yoki ochilmayapti: {e}")
        
    def __str__(self):
        return self.full_name_uz
    

class Departments(models.Model):
    image = models.ImageField(upload_to='kafedra/', null=True, blank=True, verbose_name="Direktor rasmi", help_text="Rasm o‘lchami 370x250 piksel bo‘lishi kerak!")
    titul_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi  O'zbekcha kiriting", verbose_name="Kafedra nomi")
    titul_en = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi  O'zbekcha kiriting", verbose_name="Kafedra nomi")
    titul_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Kafedra nomi  O'zbekcha kiriting", verbose_name="Kafedra nomi")

    text_uz = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_en = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")
    text_ru = models.CharField(max_length=500, null=True, blank=True, help_text="Sarlovha 500 belgi", verbose_name="Sarlovha matini:")


    full_name_uz = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", verbose_name="Kafedra muduri F.I.O:")
    full_name_en = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Englizcha kiriting", verbose_name="Kafedra muduri F.I.O:")
    full_name_ru = models.CharField(max_length=200, null=True, blank=True, help_text="Familiya Ism Otasini ism  Ruscha kiriting", verbose_name="Kafedra muduri F.I.O:")

    acceptance = models.CharField(max_length=100, null=True, blank=True, help_text="Chorshanba - Juma, 15:00 - 17:00", verbose_name="Qabul:")
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="+998901234567", verbose_name="Telefon:")
    email = models.CharField(max_length=200, null=True, blank=True, help_text="z.karshiyev@samtuit.uz, zaynidin85@gmail.com", verbose_name="Email:")
    
    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Biografiya Uzb", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Biografiya Eng", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Biografiya Rus", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Kafedra"

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

    def clean(self):
        if not self.image:
            return  # Agar rasm yuklanmagan bo'lsa, to'xtaydi

        # Super class clean metodini chaqirish
        super().clean()

        try:
            # Yuklangan rasmni ochish
            img = Image.open(self.image)
            if img.height > 250 or img.width > 370:
                raise ValidationError("Rasm o‘lchami 370x250 piksel bo‘lishi kerak!")
        except Exception as e:
            raise ValidationError(f"Yuklangan rasm noto'g'ri yoki ochilmayapti: {e}")
        
    def __str__(self):
        return self.full_name_uz
  