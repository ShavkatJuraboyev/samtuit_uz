from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import bleach

class Post(models.Model):
    title = models.CharField(max_length=200)
    content=RichTextUploadingField(config_name='extends')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    