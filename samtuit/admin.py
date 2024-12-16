from django.contrib import admin
from samtuit.models import PictureSlider, Partners, Students, Wisdom, Celebrities

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
