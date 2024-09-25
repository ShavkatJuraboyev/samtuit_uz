from django.contrib import admin
from .models import Post
from ckeditor.widgets import CKEditorWidget
from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'created_at')
    search_fields = ('title',)

admin.site.register(Post, PostAdmin)
