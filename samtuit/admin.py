from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from samtuit.models import PictureSlider, Partners, Students, Wisdom, Celebrities, Menu
from samtuit.forms import MenuAdminForm

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    class Media:
        js = ('users/js/admin.js',)

    list_display = ['title_uz', 'menu_type', 'parent', 'linked_model', 'linked_object', 'order']
    list_filter = ['parent', 'menu_type']
    list_editable = ['order']

admin.site.register(PictureSlider)

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('frist_name', 'last_name', 'candidate')

@admin.register(Wisdom)
class WisdomAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')


@admin.register(Celebrities)
class CelebritiesAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')
