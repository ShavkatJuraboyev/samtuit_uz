# Generated by Django 5.1.2 on 2025-01-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0005_departments_created_at_departments_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='leadership',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
