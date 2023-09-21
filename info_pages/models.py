import datetime
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
import urllib.parse


def upload_to(instance, filename):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")  # Генерируем строку с датой и временем
    return f"uploads/{timestamp}/{filename}"

# Create your models here.
class Photo(models.Model):
    file = models.ImageField(verbose_name='Файл', upload_to=upload_to)
    file_thumbnail_avatar = ImageSpecField(source='file',
                                      processors=[ResizeToFill(120, 120)],
                                      format='JPEG',
                                      options={'quality': 80})
    file_thumbnail_partner = ImageSpecField(source='file',
                                      processors=[ResizeToFit(height=150)],
                                      format='JPEG',
                                      options={'quality': 80})
    
    file_thumbnail_guarantes = ImageSpecField(source='file',
                                      processors=[ResizeToFill(413, 360)],
                                      format='JPEG',
                                      options={'quality': 80})

    def __str__(self):
        return self.file.name
      
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        
class PhoneNumber(models.Model):   
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    
    def __str__(self):
        return self.phone_number
    
    
    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефона'
    
class SocialNetwork(models.Model):
    supported_social_networks = [
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
        ('telegram', 'Telegram'),
        ('discord', 'Discord'),
        ('x-twitter', 'Twitter'),
        ('snapchat', 'Snapchat'),
        ('whatsapp', 'WhatsApp'),
        ('viber', 'Viber')
    ]
    link = models.CharField(max_length=64, verbose_name='URL странички в социальной сети')
    name = models.CharField(max_length=15, verbose_name='Название социальной сети', choices=supported_social_networks)
    
    def __str__(self):
        return f'{self.get_name_display()}'
    
    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

    
class ContactInfo(models.Model):
    phones = models.ManyToManyField(PhoneNumber, verbose_name="Номера телефонов")
    social_networks = models.ManyToManyField(SocialNetwork, verbose_name="Социальные сети")
    address = models.CharField(max_length=150, verbose_name='Запрос для поиска в Google Maps')
    address_url = models.CharField(max_length=150, verbose_name='URL встройки GMaps', null=True, blank=True)
    
    def __str__(self):
        return f'{self.address} | Больше не добавляйте'
    
    def generate_google_maps_embed_link(self, address):
        base_url = "https://www.google.com/maps/embed/v1/place"
        encoded_address = urllib.parse.quote(address)
        query = f"q={encoded_address}&key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8"
        embed_link = f"{base_url}?{query}"
        return embed_link
    
    def save(self, *args, **kwargs):
        if self.address:
            self.address_url = self.generate_google_maps_embed_link(self.address)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Контакты (одно поле)'
        verbose_name_plural = 'Контакты (одно поле)'
    
    
class AboutUs(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    photo = models.ForeignKey(Photo, verbose_name=("Фотография"), on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} | Больше не добавляйте'
    
    class Meta:
        verbose_name = 'О нас (одно поле)'
        verbose_name_plural = 'О нас (одно поле)'
    
    
class Guarantees(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    description = models.CharField(max_length=250, verbose_name='Описание')
    photo = models.ForeignKey(Photo, verbose_name=("Фотография"), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Гарантия'
        verbose_name_plural = 'Гарантии'
    
    
class Partners(models.Model):
    link = models.URLField(verbose_name='URL партнера (если есть)', null=True, blank=True)
    name = models.CharField(max_length=32, verbose_name='Название партнера (для удобства)', null=True, blank=True)
    photo = models.ForeignKey(Photo, verbose_name="Логотип", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
    
class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО')
    position = models.CharField(max_length=50, verbose_name='Должность')
    photo = models.ForeignKey(Photo, verbose_name="Фотограция", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'
    
    
class LegalDocument(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назание документа')
    text = models.TextField(verbose_name='Текст')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Юридический документ'
        verbose_name_plural = 'Юридические документы'
    
    