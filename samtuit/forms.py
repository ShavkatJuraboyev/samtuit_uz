# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from django import forms
# from .models import Post

# class PostForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget(config_name='extends'))

#     class Meta:
#         model = Post
#         fields = ['title', 'content']


from django import forms
from django.apps import apps
from samtuit.models import Menu

class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Menu turi - list/detail bo'lishiga qarab maydonlarni boshqarish
        menu_type = self.instance.menu_type if self.instance else None

        # Linked model ro'yxati uchun barcha modellarni olib kelish
        model_choices = [(model._meta.label, model._meta.verbose_name) for model in apps.get_models()]
        self.fields['linked_model'].widget = forms.Select(choices=[('', '--- Model tanlang ---')] + model_choices)

        if menu_type == 'detail' and self.instance.linked_model:
            # Linked object uchun, tanlangan modeldagi obyektlarni olib kelish
            model = apps.get_model(self.instance.linked_model)
            object_choices = [(obj.pk, str(obj)) for obj in model.objects.all()]
            self.fields['linked_object'].widget = forms.Select(choices=[('', '--- Obyekt tanlang ---')] + object_choices)
        else:
            # Agar "list" tanlangan bo'lsa, linked_objectni ko'rsatilmasin
            self.fields['linked_object'].widget = forms.HiddenInput()
