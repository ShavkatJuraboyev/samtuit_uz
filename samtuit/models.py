from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

class PictureSlider(models.Model):
    image = models.ImageField(upload_to="silder/")

    def __str__(self):
        return f"{self.id}-rasm"

class Post(models.Model):
    title = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True)
    content = CKEditor5Field(config_name='extends')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, editable=False)
    share_count = models.IntegerField(default=0) 

    def __str__(self):
        return self.title
    