from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserHemis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    hemis_id = models.CharField(max_length=100, unique=True, verbose_name="Hemis ID")
    phone = models.CharField(max_length=13, verbose_name="Telefon raqami")
    short_name = models.CharField(max_length=100, verbose_name="Qisqartma ismi")
    userStatus = models.CharField(max_length=100, verbose_name="Foydalanuvchi holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hemis_id
    class Meta:
        verbose_name = "Foydalanuvchilar"
        verbose_name_plural = "Foydalanuvchilar ro'yxati"

 
class GrantApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    faculty = models.CharField(max_length=100, verbose_name="Fakultet", null=True, blank=True)
    group = models.CharField(max_length=100, verbose_name="Guruh", null=True, blank=True)
    gpa_ball = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="GPA balli", null=True, blank=True)
    application_date = models.DateTimeField(auto_now_add=True, verbose_name="Ariza yuborilgan sana")
    file = models.FileField(upload_to='grant_applications/', verbose_name="Ariza fayli")
    social_activism_field = models.FileField(upload_to='social_activism/', verbose_name="Ijtimoiy faoliyat fayli", null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Kutilmoqda'), ('approved', 'Tasdiqlangan'), ('rejected', 'Rad etilgan')], default='pending', verbose_name="Ariza holati")
    new_phone = models.CharField("Yangi telefon raqam", max_length=20)
    comments = models.TextField(blank=True, null=True, verbose_name="Izohlar")

    def __str__(self):
        return f"{self.user.username} - {self.status}"

    class Meta:
        verbose_name = "Grant arizasi"
        verbose_name_plural = "Grant arizalari"



class ForeignStudent(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Familiya", null=True, blank=True)
    phone = models.CharField(max_length=13, verbose_name="Telefon raqami", null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name="Mamlakat", null=True, blank=True)
    passport_file = models.FileField(upload_to='passports/', verbose_name="Pasport fayli", null=True, blank=True)
    diploma_file = models.FileField(upload_to='diplomas/', verbose_name="Diplom fayli", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    def __str__(self):
        return (self.first_name or "Ism yo'q") + " " + (self.last_name or "Familiya yo'q")

    class Meta:
        verbose_name = "Chet el talabalari"
        verbose_name_plural = "Chet el talabalari ro'yxati"