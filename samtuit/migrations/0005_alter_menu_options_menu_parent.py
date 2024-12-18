# Generated by Django 4.2.17 on 2024-12-18 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samtuit', '0004_menu_linked_model_menu_linked_object_menu_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['parent__id', 'order'], 'verbose_name': 'Menyu', 'verbose_name_plural': 'Menyular'},
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='samtuit.menu', verbose_name='Ota menyu'),
        ),
    ]
