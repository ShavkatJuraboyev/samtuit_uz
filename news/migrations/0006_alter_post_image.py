# Generated by Django 5.1.2 on 2025-01-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_announcements_content_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Rasm o‘lchami 740x500 piksel bo‘lishi kerak!', null=True, upload_to='images/', verbose_name='Sarlovha rasmi'),
        ),
    ]
