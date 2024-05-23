# Generated by Django 4.2.4 on 2023-09-01 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0008_remove_view_date_view_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='date_time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]