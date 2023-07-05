# Generated by Django 4.2.1 on 2023-07-05 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='views',
        ),
        migrations.AlterField(
            model_name='view',
            name='date_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='views',
            field=models.ManyToManyField(to='main.view'),
        ),
    ]
