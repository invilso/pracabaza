# Generated by Django 4.2.1 on 2023-05-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_sex_remove_vacancy_sex_vacancy_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='price',
            field=models.FloatField(verbose_name='Ставка(zlot)'),
        ),
    ]
