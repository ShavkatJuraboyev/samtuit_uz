from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='extends'))

    class Meta:
        model = Post
        fields = ['title', 'content']
