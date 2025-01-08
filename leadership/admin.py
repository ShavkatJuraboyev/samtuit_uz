from django.contrib import admin
from leadership.models import Leadership, Departments, DepartmentsCenter, Faculty, FacultyDean
# Register your models here.

@admin.register(Leadership)
class AdminLeadership(admin.ModelAdmin):
    list_display = ('full_name_uz', 'full_name_en', 'full_name_ru', 'created_at', 'created_by', 'positions')
    search_fields = ('full_name_uz',)
    readonly_fields = ('created_at', 'created_by') 
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'acceptance','phone','email','positions', 'created_by',),
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
    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(AdminLeadership, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields


@admin.register(Departments)
class AdminDepatmentd(admin.ModelAdmin):
    list_display = ('titul_uz', 'titul_en', 'titul_ru', 'created_at', 'created_by')
    search_fields = ('titul_uz', 'titul_en', 'titul_ru',)
    readonly_fields = ('created_at', 'created_by') 
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'faculty', 'created_by',),
        }),
        ('Uzbekcha maʼlumotlar', {
            'fields': ('titul_uz', 'text_uz', 'content_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('titul_en', 'text_en', 'content_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('titul_ru', 'text_ru', 'content_ru', 'slug',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(AdminDepatmentd, self).save_model(request, obj, form, change)  # Bu yerda `AdminDepatmentd` ishlatiladi

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields


@admin.register(DepartmentsCenter)
class AdminDepatmentdCenter(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru', 'created_at', 'created_by')
    search_fields = ('title_uz', 'title_en', 'title_ru',)
    readonly_fields = ('created_at', 'created_by') 
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'created_by',),
        }),
        ('Uzbekcha maʼlumotlar', {
            'fields': ('title_uz', 'text_uz', 'content_uz',),
        }),
        ('Inglizcha maʼlumotlar', {
            'fields': ('title_en', 'text_en', 'content_en',),
        }),
        ('Ruscha maʼlumotlar', {
            'fields': ('title_ru', 'text_ru', 'content_ru', 'slug',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(AdminDepatmentdCenter, self).save_model(request, obj, form, change)  # Bu yerda `AdminDepatmentdCenter` ishlatiladi

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields
    
@admin.register(Faculty)
class AdminFaculty(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru', 'created_at', 'created_by')
    search_fields = ('title_uz', 'title_en', 'title_ru',)
    readonly_fields = ('created_at', 'created_by') 
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
            'fields': ('title_ru', 'text_ru', 'slug',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(AdminFaculty, self).save_model(request, obj, form, change)  # Bu yerda `AdminFaculty` ishlatiladi

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields
    
@admin.register(FacultyDean)
class AdminFacultyDean(admin.ModelAdmin):
    list_display = ('full_name_uz', 'full_name_en', 'full_name_ru', 'created_at', 'created_by', 'positions')
    search_fields = ('full_name_uz',)
    readonly_fields = ('created_at', 'created_by') 
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('image', 'faculty', 'acceptance','phone','email','positions', 'created_by',),
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
    def save_model(self, request, obj, form, change):
        """Admin foydalanuvchisi bo'lganligi uchun created_by maydonini avtomatik to'ldirish."""
        if not obj.pk:  # Ob'ekt yangi bo'lsa
            obj.created_by = request.user
        super(AdminFacultyDean, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """created_by maydonini faqat ko'rish uchun qilib qo'yish."""
        if obj: 
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields