# Generated by Django 5.1.2 on 2024-12-24 07:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samtuit', '0014_postone_alter_lists_text_en_alter_lists_text_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postone',
            name='content2',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]
