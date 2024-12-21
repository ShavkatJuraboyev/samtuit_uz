from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from samtuit.models import PictureSlider, Partners, Students, Wisdom, Celebrities, Menu, Season, Lists, ListsMenu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru', 'parent')  # Ko'rsatiladigan ustunlar
    list_filter = ('parent',)  # Filtrlar uchun 'parent' ni to'g'ri qo'llash
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    fieldsets = (
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru',),
        }),
        ('Umumiy maʼlumotlar', {
            'fields': ('url', 'parent'),  # parent maydonini umumiy ma'lumotlar qismiga qo'shish
        }),
    )

admin.site.register(PictureSlider)
admin.site.register(Season)

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('frist_name', 'last_name', 'candidate')

@admin.register(Wisdom)
class WisdomAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru', 'created_by')
    list_filter = ('title_uz', 'title_en', 'title_ru')  
    search_fields = ('title_uz', 'title_en', 'title_ru')
    readonly_fields = ('created_by',) 
    fieldsets = (
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz', 'text_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en', 'text_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru', 'text_ru',),
        }),
        ('O\'zgarmas maʼlumotlar', {
            'fields': ('created_by',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(WisdomAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

@admin.register(Celebrities)
class CelebritiesAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')
    readonly_fields = ('created_by',) 
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'created_by',),
        }),
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz', 'text_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en', 'text_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru', 'text_ru',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(CelebritiesAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields


# Inline modeli Lists uchun
class ListsInline(admin.TabularInline):
    model = Lists
    extra = 1  # Qo'shimcha bo'sh qatordan nechta bo'lishi kerakligini belgilang
    fields = ('title_uz', 'image', 'created_at')
    readonly_fields = ('created_at',)  # Faqat o'qish uchun maydonlar
    show_change_link = True  # Inline'lar uchun tahrirlash havolasini ko'rsatish

# ListsMenu uchun konfiguratsiya
@admin.register(ListsMenu)
class ListsMenuAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'slug')  # Admin panelda ko'rinadigan ustunlar
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydoni
    list_filter = ('title_uz', 'title_en', 'title_ru')  # Filtrlar
    prepopulated_fields = {'slug': ('title_en',)}  # Slug maydoni avtomatik to'ldiriladi
    # inlines = [ListsInline]  # Lists Inline qo'shiladi

# Lists uchun konfiguratsiya
@admin.register(Lists)
class ListsAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'listmenu', 'created_at', 'created_by', 'share_count')  # Ko'rsatiladigan ustunlar
    list_filter = ('listmenu', 'created_at')  # Filtrlar
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('created_at', 'share_count', 'created_by',)  # Faqat o'qish uchun maydonlar
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('listmenu', 'image', 'url', 'share_count', 'created_by'),
        }),
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz', 'text_uz', 'content_uz'),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en', 'text_en', 'content_en'),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru', 'text_ru', 'content_ru'),
        }),
    )
    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(ListsAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields
    # save_on_top = True  # Saqlash tugmalari yuqorida ko'rsatiladi