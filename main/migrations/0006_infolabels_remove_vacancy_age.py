# Generated by Django 4.2.1 on 2023-05-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_vacancy_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoLabels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Текст информационной таблички')),
            ],
            options={
                'verbose_name': 'Информационная табличка',
                'verbose_name_plural': 'Информационные таблички',
            },
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='age',
        ),
    ]