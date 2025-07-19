from django.contrib import admin
from .models import GrantApplication

@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'application_date', 'new_phone', 'status', 'gpa_ball')  # Admin jadvalda ko‘rsatiladigan ustunlar
    list_filter = ('status', 'application_date', 'gpa_ball')  # Chap tomonda filter bo‘lishi
    search_fields = ('user__username', 'new_phone')  # Qidiruv uchun maydonlar
    readonly_fields = ('application_date',)  # O‘zgartirib bo‘lmaydigan maydon
