# Generated by Django 4.2.1 on 2023-07-01 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_vacancy_active_vacancy_views_alter_vacancy_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=300, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='sex',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Пол'),
        ),
    ]