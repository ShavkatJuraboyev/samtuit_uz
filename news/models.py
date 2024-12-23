from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.templatetags.static import static
from django.utils.text import slugify


class Post(models.Model): 
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")

    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini")

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Yangiliklar"
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_post_title(self, language):
        return self.get_translation('title', language)

    def get_post_text(self, language):
        return self.get_translation('text', language)

    def get_post_content(self, language):
        return self.get_translation('content', language)

    def get_post_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Post.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Post.DoesNotExist:
            pass
        super(Post, self).save(*args, **kwargs)

 
class Meeting(models.Model):
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Yig'ilishlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_meeting_title(self, language):
        return self.get_translation('title', language)

    def get_meeting_text(self, language):
        return self.get_translation('text', language)

    def get_meeting_content(self, language):
        return self.get_translation('content', language)

    def get_meet_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Meeting.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Meeting.DoesNotExist:
            pass
        super(Meeting, self).save(*args, **kwargs)
 

class Announcements(models.Model): 
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    location = models.CharField(max_length=200, null=True, verbose_name="Unversitet")
    build = models.CharField(max_length=200, null=True, verbose_name="Manzil")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Tadbir rasmi")
    day = models.DateField(verbose_name="Kun", help_text="Tadbir qaysi kunda bo'lishini kiriting", null=True)
    start_time = models.TimeField(verbose_name="Boshlanish vaqti", help_text="Tadbir boshlanish vaqtini kiriting (HH:MM:SS)", null=True)
    end_time = models.TimeField(verbose_name="Tugash vaqti", help_text="Tadbir tugash vaqtini kiriting (HH:MM:SS)", null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)

    class Meta:
        verbose_name_plural = "E'lonlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_anno_title(self, language):
        return self.get_translation('title', language)

    def get_anno_text(self, language):
        return self.get_translation('text', language)

    def get_anno_content(self, language):
        return self.get_translation('content', language)

    def get_elon_img(self):
        return self.image.url if self.image else static('')

    def __str__(self):
        return f"{self.title_uz}"
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Announcements.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Announcements.DoesNotExist:
            pass

        super(Announcements, self).save(*args, **kwargs)


class Designation(models.Model):
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Uchrashuvlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_desig_title(self, language):
        return self.get_translation('title', language)

    def get_desig_text(self, language): 
        return self.get_translation('text', language)

    def get_desig_content(self, language):
        return self.get_translation('content', language)

    def get_desig_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Designation.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Designation.DoesNotExist:
            pass
        super(Designation, self).save(*args, **kwargs)


class PressConference(models.Model):
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Matbuot anjumanlar"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_press_title(self, language):
        return self.get_translation('title', language)

    def get_press_text(self, language):
        return self.get_translation('text', language)

    def get_press_content(self, language):
        return self.get_translation('content', language)

    def get_pres_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = PressConference.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except PressConference.DoesNotExist:
            pass
        super(PressConference, self).save(*args, **kwargs)


class Seminar(models.Model):
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Seminarlar"
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_semin_title(self, language):
        return self.get_translation('title', language)

    def get_semin_text(self, language):
        return self.get_translation('text', language)

    def get_semin_content(self, language):
        return self.get_translation('content', language)

    def get_semin_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Seminar.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Seminar.DoesNotExist:
            pass
        super(Seminar, self).save(*args, **kwargs)


class Conversation(models.Model):
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text_uz = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True)

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    text_en = models.CharField(max_length=500, null=True, help_text="English sarlavha matini maksimal 500 belgi", verbose_name="English sarlovha matini")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    text_ru = models.CharField(max_length=500, null=True, help_text="Ruscha sarlavha matini maksimal 500 belgi", verbose_name="Ruscha arlovha matini")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Davra suxbatlari"

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))

    def get_conv_title(self, language):
        return self.get_translation('title', language)

    def get_conv_text(self, language):
        return self.get_translation('text', language)

    def get_conv_content(self, language):
        return self.get_translation('content', language)

    def get_semin_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title_uz
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = Conversation.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Conversation.DoesNotExist:
            pass
        super(Conversation, self).save(*args, **kwargs)

class Details(models.Model): 
    title_uz = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    content_uz = CKEditor5Field(config_name='extends_uz', verbose_name="Sarlovha umumiy matini")

    title_en = models.CharField(max_length=200, null=True, help_text="English sarlavha maksimal 200 belgi", verbose_name="English sarlovhasi")
    content_en = CKEditor5Field(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True)

    title_ru = models.CharField(max_length=200, null=True, help_text="Ruscha sarlavha maksimal 200 belgi", verbose_name="Ruscha arlovhasi")
    content_ru = CKEditor5Field(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True)

    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz
    
    class Meta:
        verbose_name_plural = "Bittalik ma'lumotlar"
    
    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"  # Masalan: '_en'
        translated_field = f"{field_name}{language_suffix}"  # Masalan: 'title_en'
        # Agar kerakli til bo'yicha ma'lumot topilmasa, O'zbek tilini qaytaradi
        return getattr(self, translated_field, getattr(self, f"{field_name}_uz", ''))
    
    def get_detail_title(self, language):
        return self.get_translation('title', language)

    def get_detail_content(self, language):
        return self.get_translation('content', language)