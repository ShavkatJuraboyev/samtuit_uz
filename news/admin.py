from django.contrib import admin
from news.models import Post, Meeting,  Announcements, Designation, PressConference, Seminar, Conversation


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
    prepopulated_fields = {"slug": ("title_uz",)}

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
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
 
@admin.register(Announcements)
class Announc(admin.ModelAdmin):
    list_display = ('title_uz', 'location', 'build', 'day')
    list_filter = ('day',)
    search_fields = ('name',)
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

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
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
    
@admin.register(PressConference)
class PressConferenceAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
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

@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
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

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by')
    search_fields = ('title_uz',)
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
   