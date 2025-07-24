from django.contrib import admin
from news.models import Post, Meeting,  Announcements, Designation, PressConference, Seminar, Conversation, Details
from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'ip_address', 'mac_address', 'device')
    search_fields = ['user__username', 'content_type__model']

    def log_change(self, request, object, message):
        ip = getattr(request, 'client_ip', 'N/A')
        mac = getattr(request, 'mac_address', 'N/A')
        device = getattr(request, 'user_agent_str', 'N/A')

        # Ma’lumotlarni message ichida saqlaymiz
        message += f" | IP: {ip} | MAC: {mac} | Device: {device}"

        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=None,
            object_id=None,
            object_repr=str(object),
            action_flag=LogEntry.CHANGE,
            change_message=message
        )

    def ip_address(self, obj):
        if "IP:" in obj.change_message:
            parts = obj.change_message.split(" | ")
            for part in parts:
                if part.strip().startswith("IP:"):
                    return part.replace("IP: ", "").strip()
        return "N/A"

    def mac_address(self, obj):
        if "MAC:" in obj.change_message:
            parts = obj.change_message.split(" | ")
            for part in parts:
                if part.strip().startswith("MAC:"):
                    return part.replace("MAC: ", "").strip()
        return "N/A"

    def device(self, obj):
        if "Device:" in obj.change_message:
            parts = obj.change_message.split(" | ")
            for part in parts:
                if part.strip().startswith("Device:"):
                    return part.replace("Device: ", "").strip()
        return "N/A"

    ip_address.short_description = "IP Address"
    mac_address.short_description = "MAC Address"
    device.short_description = "Device"
    
# Admin-da LogEntry modelini ko‘rish uchun uni ro‘yxatdan o‘tkazish
admin.site.register(LogEntry, LogEntryAdmin)




@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
        super(PostAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
    list_display = ('title_uz', 'location', 'build', 'day', 'created_at', 'created_by')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    list_filter = ('title_uz', 'title_en', 'title_ru','day',)
    readonly_fields = ('created_by',) 
    fieldsets = (
        ('Umumiy sozlama', {
            'fields':('image','location', 'build', 'day', 'start_time', 'end_time', 'created_at')
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
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
    list_display = ('title_uz', 'created_at', 'created_by', 'share_count')
    search_fields = ('title_uz', 'title_en', 'title_ru')  # Qidiruv maydonlari
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Umumiy maʼlumotlar', {
            'fields': ('image', 'share_count', 'created_by', 'created_at'),
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
        if not obj.pk: 
            obj.created_by = request.user  
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields
    
@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'title_en', 'created_at', 'created_by')
    search_fields = ('title_uz', 'title_ru', 'title_en',)
    prepopulated_fields = {"slug": ("title_en",)}
    readonly_fields = ('share_count', 'created_by') 
    fieldsets = (
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz',  'content_uz', 'created_at'),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en', 'content_en'),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru', 'content_ru'),
        }),
        ('O\'zgarmas maʼlumotlar', {
            'fields': ('slug','share_count', 'created_by'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(DetailsAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields
    