# Generated by Django 4.2.4 on 2024-04-01 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_pages', '0007_aboutus_text_az_aboutus_text_en_aboutus_text_pl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetwork',
            name='name_az',
        ),
        migrations.RemoveField(
            model_name='socialnetwork',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='socialnetwork',
            name='name_pl',
        ),
        migrations.RemoveField(
            model_name='socialnetwork',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='socialnetwork',
            name='name_uk',
        ),
    ]
