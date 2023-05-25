# Generated by Django 4.2.1 on 2023-05-25 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_index_alter_vacancy_options_alter_state_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='category',
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.state', verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.index', verbose_name='Индекс'),
        ),
    ]
