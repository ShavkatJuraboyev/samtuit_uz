from django.contrib import admin
from leadership.models import Leadership
# Register your models here.

@admin.register(Leadership)
class AdminLeadership(admin.ModelAdmin):
    list_display = ('full_name_uz', 'full_name_en', 'full_name_ru')
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'acceptance','phone','email','positions',),
        }),
        ('Uzbekcha maʼlumotlar', {
            'fields': ('full_name_uz', 'position_uz', 'content_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('full_name_en', 'position_en', 'content_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('full_name_ru', 'position_ru', 'content_ru', 'slug',),
        }),
    )