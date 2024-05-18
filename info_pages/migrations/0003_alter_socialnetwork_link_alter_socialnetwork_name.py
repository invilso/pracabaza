# Generated by Django 4.2.4 on 2023-09-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_pages', '0002_alter_partners_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='link',
            field=models.CharField(max_length=64, verbose_name='URL странички в социальной сети'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='name',
            field=models.CharField(choices=[('facebook', 'Facebook'), ('pinterest', 'Pinterest'), ('instagram', 'Instagram'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('linkedin', 'LinkedIn'), ('telegram', 'Telegram'), ('discord', 'Discord'), ('x-twitter', 'Twitter'), ('snapchat', 'Snapchat'), ('whatsapp', 'WhatsApp'), ('viber', 'Viber')], max_length=15, verbose_name='Название социальной сети'),
        ),
    ]
