# Generated by Django 5.1.2 on 2025-01-08 08:05

import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0008_faculty_departments_faculty'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyDean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name_uz', models.CharField(blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", max_length=200, null=True, verbose_name="To'liq F.I.O Uzb:")),
                ('full_name_en', models.CharField(blank=True, help_text='Familiya Ism Otasini ism  Englizcha kiriting', max_length=200, null=True, verbose_name="To'liq F.I.O Eng:")),
                ('full_name_ru', models.CharField(blank=True, help_text='Familiya Ism Otasini ism  Ruscha kiriting', max_length=200, null=True, verbose_name="To'liq F.I.O Rus:")),
                ('image', models.ImageField(blank=True, help_text='Rasm o‘lchami 270x201 piksel bo‘lishi kerak!', null=True, upload_to='rektorat/', verbose_name='Direktor rasmi')),
                ('acceptance', models.CharField(blank=True, help_text='Chorshanba - Juma, 15:00 - 17:00', max_length=100, null=True, verbose_name='Qabul:')),
                ('phone', models.CharField(blank=True, help_text='+998901234567', max_length=20, null=True, verbose_name='Telefon:')),
                ('email', models.CharField(blank=True, help_text='z.karshiyev@samtuit.uz, zaynidin85@gmail.com', max_length=200, null=True, verbose_name='Email:')),
                ('content_uz', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Biografiya Uzb')),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Biografiya Eng')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Biografiya Rus')),
                ('positions', models.CharField(choices=[('dekan', 'Dekan'), ("o'rinbosar", "O'rinbosar")], max_length=20, verbose_name='Lavozim nomi:')),
                ('position_uz', models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Uzb nomi:')),
                ('position_en', models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Eng nomi:')),
                ('position_ru', models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Rus nomi:')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leadership.faculty', verbose_name='Fakultet:')),
            ],
            options={
                'verbose_name_plural': 'Rektorat',
            },
        ),
    ]
