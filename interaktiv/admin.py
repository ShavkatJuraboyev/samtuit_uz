from django.contrib import admin
from .models import GrantApplication, ForeignStudent, Re_Application

@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'application_date', 'new_phone', 'status', 'gpa_ball')  # Admin jadvalda ko‘rsatiladigan ustunlar
    list_filter = ('status', 'application_date', 'gpa_ball')  # Chap tomonda filter bo‘lishi
    search_fields = ('user__username', 'new_phone')  # Qidiruv uchun maydonlar
    readonly_fields = ('application_date',)  # O‘zgartirib bo‘lmaydigan maydon

@admin.register(ForeignStudent)
class ForeignStudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'phone')
    readonly_fields = ('created_at',)  # O‘zgartirib bo‘lmaydigan maydon

@admin.register(Re_Application)
class Re_ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'is_gpa_updated', 'is_manaviyat_updated', 'status')
    list_filter = ('status', 'is_gpa_updated', 'is_manaviyat_updated')
    search_fields = ('user__username', 'reason')