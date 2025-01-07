# Generated by Django 5.1.2 on 2025-01-07 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadership',
            name='position_en',
            field=models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Eng nomi:'),
        ),
        migrations.AddField(
            model_name='leadership',
            name='position_ru',
            field=models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Rus nomi:'),
        ),
        migrations.AddField(
            model_name='leadership',
            name='position_uz',
            field=models.CharField(blank=True, help_text='Lavozimini yozing', max_length=500, null=True, verbose_name='Lavozim Uzb nomi:'),
        ),
        migrations.AlterField(
            model_name='leadership',
            name='positions',
            field=models.CharField(choices=[('rektor', 'Rektor'), ("o'rinbosar", "O'rinbosar")], max_length=20, verbose_name='Lavozim nomi:'),
        ),
    ]
