# Generated by Django 5.1.2 on 2024-12-18 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('samtuit', '0002_celebrities_wisdom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='celebrities',
            options={'verbose_name_plural': "Mashur so'zlar"},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'Menyu', 'verbose_name_plural': 'Menyular'},
        ),
        migrations.RemoveField(
            model_name='menu',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='url',
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_type',
            field=models.CharField(choices=[('list', 'List Ko‘rinishda'), ('detail', 'Detail Ko‘rinishda')], default='list', max_length=10, verbose_name='Menyu turi'),
        ),
        migrations.AddField(
            model_name='menu',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Faolmi?'),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Bog‘lanadigan ID (optional)')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name="Bog‘lanadigan Model (Ma'lumot turi)")),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='samtuit.menu', verbose_name='Menyu')),
            ],
            options={
                'verbose_name': 'Menyu elementi',
                'verbose_name_plural': 'Menyu elementlari',
            },
        ),
    ]
