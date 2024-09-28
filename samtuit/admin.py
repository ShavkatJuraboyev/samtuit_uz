from django.contrib import admin
from .models import Post, PictureSlider
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),
        }

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'created_at', 'created_by')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk: 
            obj.created_by = request.user  
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

admin.site.register(Post, PostAdmin)
admin.site.register(PictureSlider)
