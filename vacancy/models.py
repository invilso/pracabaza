import re
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from info_pages.models import upload_to

class InvalidLink(Exception):
    pass

def extract_youtube_video_id(url):
    # Регулярное выражение для извлечения идентификатора видео из ссылок на YouTube
    regex = r"(?:youtube\.com/watch\?v=|youtu.be/|youtube.com/watch\?.*v=)([\w-]+)"
    match = re.search(regex, url)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None

def create_youtube_embedded(link, width=560, height=315):
    link = extract_youtube_video_id(link)
    if not link:
        raise InvalidLink('Error! Not a valid link youtube.')
    html = '<iframe class="embed-responsive-item" src="https://www.youtube.com/embed/'+link+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    return html

class State(models.Model):
    name = models.CharField(verbose_name='Название', max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class City(models.Model):
    name = models.CharField(verbose_name="Название города", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Sex(models.Model):
    name = models.CharField(verbose_name='Пол', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'
  
class InfoLabel(models.Model):
    house = models.CharField(max_length=512, verbose_name='Жилье')
    benefits = models.CharField(max_length=512, verbose_name='Выгоды')

    def __str__(self):
        return f'{self.house[:50]}|{self.benefits[:50]}'

    class Meta:
        verbose_name = 'Описание Стандарт'
        verbose_name_plural = 'Описания Стандарт'
  
class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
  
class Index(models.Model):
    name = models.CharField(verbose_name='Индекс', max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Индекс'
        verbose_name_plural = 'Индексы'
        
        
class Photo(models.Model):
    file = models.ImageField(verbose_name='Файл', upload_to=upload_to)
    file_thumbnail_list = ImageSpecField(source='file',
                                      processors=[ResizeToFill(432, 153)],
                                      format='JPEG',
                                      options={'quality': 70})
    file_thumbnail_deck = ImageSpecField(source='file',
                                      processors=[ResizeToFill(366, 206)],
                                      format='JPEG',
                                      options={'quality': 95})

    def __str__(self):
        return self.file.name
      
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        
class Video(models.Model):
    file = models.FileField(verbose_name='Файл (Если нет ссылки на YT)', null=True, blank=True, upload_to=upload_to)
    url = models.URLField(verbose_name='Ссылка на YouTube (если есть)', null=True, blank=True)
    embeded = models.CharField(max_length=500, verbose_name='Встройка в YouTube (не изменять)', null=True, blank=True)

    def __str__(self):
        return self.file or self.url

    def save(self, *args, **kwargs):
        if self.url:
            self.embeded = create_youtube_embedded(self.url)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Видеозапись'
        verbose_name_plural = 'Видеозаписи'
        
class WorkDuty(models.Model):
    description = models.TextField(verbose_name='Описание обязанности', unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Обязанность по работе'
        verbose_name_plural = 'Обязанности по работе'
        
class HourlyPaymentOption(models.Model):
    payment_type = models.CharField(max_length=100, verbose_name='Тип оплаты (для студентов, ночные, испытательный и тд.)')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Почасовая ставка')

    def __str__(self):
        return f"{self.payment_type}: {self.hourly_rate} zl/час"

    class Meta:
        verbose_name = 'Вариант почасовой оплаты'
        verbose_name_plural = 'Варианты почасовой оплаты'

class View(models.Model):
    ip = models.CharField(max_length=64, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    region_name = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    isp = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.BooleanField(blank=True, null=True)

class Vacancy(models.Model):
    name = models.CharField(verbose_name='Название вакансии', max_length=300)
    title = models.CharField(verbose_name='Заголовок вакансии', max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Место работы")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="Регион")
    card_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Картинка карточки вакансии и обложки", related_name='vacancy_card_photo')
    photos = models.ManyToManyField(Photo, verbose_name='Фотографии вакансии')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видеозапись вакансии', null=True, blank=True)
    info_label = models.ForeignKey(InfoLabel, on_delete=models.SET_NULL, verbose_name="Описание стандарт", null=True, blank=True)
    salary_per_hour = models.ManyToManyField(HourlyPaymentOption, verbose_name="Варианты почасовой оплаты")
    salary_per_mounth_min = models.IntegerField(verbose_name='Ставка месячная минимум (zlot)', null=True, blank=True)
    salary_per_mounth_max = models.IntegerField(verbose_name='Ставка месячная максимум (zlot)', null=True, blank=True)
    salary_per_mounth_fixed = models.IntegerField(verbose_name='Ставка месячная фиксированая (если нет минимума или максимума) (zlot)', null=True, blank=True)
    salary_per_hour_fixed = models.FloatField(verbose_name='Ставка почасовая (если нет месячной) (zlot)', null=True, blank=True)
    salary_is_netto = models.BooleanField(verbose_name='Зарплата netto?', default=True)
    work_duties = models.ManyToManyField(WorkDuty, verbose_name='Обязанности по работе')
    work_schedule = models.TextField(verbose_name='График работы', blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    sex = models.ManyToManyField(Sex, verbose_name='Пол')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    index = models.ForeignKey(Index, on_delete=models.CASCADE, verbose_name="Индекс (служебное)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    active = models.BooleanField(verbose_name='Активно', default=True)
    views = models.ManyToManyField(View, blank=True)
    
    def _get_salary_text(self, is_netto_text):
        if self.salary_per_mounth_fixed is not None:
            return f"{self.salary_per_mounth_fixed} zł"
        elif self.salary_per_mounth_min is not None and self.salary_per_mounth_max is not None:
            return f"{self.salary_per_mounth_min} - {self.salary_per_mounth_max} zł"
        elif self.salary_per_mounth_min is not None:
            return f"от {self.salary_per_mounth_min} zł"
        elif self.salary_per_mounth_max is not None:
            return f"до {self.salary_per_mounth_max} zł"
        elif self.salary_per_hour_fixed:
            if not self.salary_per_hour_fixed.is_integer():
                return f"{self.salary_per_hour_fixed:5.2f} zł/час {is_netto_text}"
            return f"{int(self.salary_per_hour_fixed)} zł/час {is_netto_text}"
        else:
            return ""
    
    def get_salary_text_list(self):
        return self._get_salary_text('')

    
    def get_salary_text(self):
        is_netto_text = 'brutto'
        if self.salary_is_netto:
            is_netto_text = 'netto'
        return self._get_salary_text(is_netto_text)

    def __str__(self):
        return f'{self.index} - {self.name} | {self.city}'
    
    def embeded(self):
        return self.video.embeded if self.video else ""

    embeded.short_description = 'Встройка в YouTube'

    class Meta:
        ordering = ['name']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'