from django.contrib import admin
from samtuit.models.models import PictureSlider, Partners, Students, Menu

class MenuAdmin(admin.ModelAdmin):
    # Formda ko'rsatiladigan ustunlar
    list_display = ('title_uz', 'title_ru', 'title_en', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_editable = ('is_active',)

    # Admin sahifasida menyu nomini tanlash
    def get_menu_title(self, obj):
        # 'language' orqali tilni tanlab, menyu nomini olish
        # Adminda, faqat tilni ko'rsatamiz, masalan 'title_uz'
        language = 'uz'  # Agar hohlasangiz, bu o'zgaruvchiga `request`dan tilni olib qo'yishingiz mumkin
        return obj.get_menu_title(language)
    get_menu_title.short_description = 'Menyu nomi'

    # Menyu nomini ko'rsatadigan ustunni qo'shamiz
    readonly_fields = ('get_menu_title',)

    # Qidirish va tartibga solish uchun foydalanish mumkin bo'lgan maydonlar
    fieldsets = (
        (None, {
            'fields': ('title_uz', 'title_ru', 'title_en', 'url', 'parent', 'is_active')
        }),
        ('Tarjimalar', {
            'fields': ('get_menu_title',)
        }),
    )

    # Menyu nomini admin panelida o'zgartirish uchun maxsus xususiyat
    def save_model(self, request, obj, form, change):
        # Hozirgi tilni hisobga olib, menyu nomini saqlash
        super().save_model(request, obj, form, change)

# Admin paneliga Menu modelini qo'shamiz
admin.site.register(Menu, MenuAdmin)

admin.site.register(PictureSlider)

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('frist_name', 'last_name', 'candidate')