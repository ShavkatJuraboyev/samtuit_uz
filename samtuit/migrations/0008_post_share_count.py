# Generated by Django 5.1.1 on 2024-09-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samtuit', '0007_post_text_alter_post_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='share_count',
            field=models.IntegerField(default=0),
        ),
    ]