# Generated by Django 4.2.4 on 2024-02-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0012_alter_vacancy_requirements'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='actual',
            field=models.BooleanField(default=True, verbose_name='Актуально'),
        ),
    ]
