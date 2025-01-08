# Generated by Django 5.1.2 on 2025-01-08 05:51

import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0006_alter_departments_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='titul_en',
            field=models.CharField(blank=True, help_text='Kafedra nomi Englizcha kiriting', max_length=200, null=True, verbose_name='Kafedra nomi ENG'),
        ),
        migrations.AlterField(
            model_name='departments',
            name='titul_ru',
            field=models.CharField(blank=True, help_text='Kafedra nomi Ruscha kiriting', max_length=200, null=True, verbose_name='Kafedra nomi RUS'),
        ),
        migrations.AlterField(
            model_name='departments',
            name='titul_uz',
            field=models.CharField(blank=True, help_text="Kafedra nomi O'zbekcha kiriting", max_length=200, null=True, verbose_name='Kafedra nomi UZB'),
        ),
        migrations.AlterField(
            model_name='leadership',
            name='full_name_en',
            field=models.CharField(blank=True, help_text='Familiya Ism Otasini ism  Englizcha kiriting', max_length=200, null=True, verbose_name="To'liq F.I.O Eng:"),
        ),
        migrations.AlterField(
            model_name='leadership',
            name='full_name_ru',
            field=models.CharField(blank=True, help_text='Familiya Ism Otasini ism  Ruscha kiriting', max_length=200, null=True, verbose_name="To'liq F.I.O Rus:"),
        ),
        migrations.AlterField(
            model_name='leadership',
            name='full_name_uz',
            field=models.CharField(blank=True, help_text="Familiya Ism Otasini ism  O'zbekcha kiriting", max_length=200, null=True, verbose_name="To'liq F.I.O Uzb:"),
        ),
        migrations.CreateModel(
            name='DepartmentsCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Rasm o‘lchami 370x250 piksel bo‘lishi kerak!', null=True, upload_to='kafedra/', verbose_name="Bo'lim va markazlar rasmi")),
                ('title_uz', models.CharField(blank=True, help_text="Bo'lim va markazlar nomi O'zbekcha kiriting", max_length=200, null=True, verbose_name="Bo'lim va markazlar nomi UZB")),
                ('title_en', models.CharField(blank=True, help_text="Bo'lim va markazlar nomi Englizcha kiriting", max_length=200, null=True, verbose_name="Bo'lim va markazlar nomi ENG")),
                ('title_ru', models.CharField(blank=True, help_text="Bo'lim va markazlar nomi Ruscha kiriting", max_length=200, null=True, verbose_name="Bo'lim va markazlar nomi RUS")),
                ('text_uz', models.CharField(blank=True, help_text='Sarlovha 500 belgi', max_length=500, null=True, verbose_name='Sarlovha matini:')),
                ('text_en', models.CharField(blank=True, help_text='Sarlovha 500 belgi', max_length=500, null=True, verbose_name='Sarlovha matini:')),
                ('text_ru', models.CharField(blank=True, help_text='Sarlovha 500 belgi', max_length=500, null=True, verbose_name='Sarlovha matini:')),
                ('content_uz', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name="Bo'lim va markazlar ma'limot Uzb")),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name="Bo'lim va markazlar ma'limot Eng")),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name="Bo'lim va markazlar ma'limot Rus")),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Bo'lim va markazlar",
            },
        ),
    ]
