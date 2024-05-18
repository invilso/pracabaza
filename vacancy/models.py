from decimal import Decimal
import re
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from info_pages.models import upload_to
from django.utils.translation import gettext as _

class InvalidLink(Exception):
    pass

CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('UAH', 'Hryvnia'),
    ('USD', 'US Dollar'),
    ('PLN', 'Polish Złoty'),
)

CURRENCY_SYMBOLS = {
    'EUR': '€',
    'UAH': '₴',
    'USD': '$',
    'PLN': 'zł',
}

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
    name = models.CharField(verbose_name=_('Название'), max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

class City(models.Model):
    name = models.CharField(verbose_name=_("Название города"), max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

class Sex(models.Model):
    name = models.CharField(verbose_name=_('Пол'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Пол')
        verbose_name_plural = _('Пол')
  
class InfoLabel(models.Model):
    house = models.CharField(max_length=512, verbose_name=_('Жилье'))
    benefits = models.CharField(max_length=512, verbose_name=_('Выгоды'))

    def __str__(self):
        return f'{self.house[:50]}|{self.benefits[:50]}'

    class Meta:
        verbose_name = _('Описание Стандарт')
        verbose_name_plural = _('Описания Стандарт')
  
class Category(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
  
class Index(models.Model):
    name = models.CharField(verbose_name=_('Индекс'), max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Индекс')
        verbose_name_plural = _('Индексы')
        
        
class Photo(models.Model):
    file = models.ImageField(verbose_name=_('Файл'), upload_to=upload_to)
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
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
        
class Video(models.Model):
    file = models.FileField(verbose_name=_('Файл (Если нет ссылки на YT)'), null=True, blank=True, upload_to=upload_to)
    url = models.URLField(verbose_name=_('Ссылка на YouTube (если есть)'), null=True, blank=True)
    embeded = models.CharField(max_length=500, verbose_name=_('Встройка в YouTube (не изменять)'), null=True, blank=True)

    def __str__(self):
        return self.file or self.url

    def save(self, *args, **kwargs):
        if self.url:
            self.embeded = create_youtube_embedded(self.url)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Видеозапись')
        verbose_name_plural = _('Видеозаписи')
        
class WorkDuty(models.Model):
    description = models.TextField(verbose_name=_('Описание обязанности'), unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Обязанность по работе')
        verbose_name_plural = _('Обязанности по работе')
        
class Requirement(models.Model):
    description = models.TextField(verbose_name=_('Описание требования'), unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Требование к кандидату')
        verbose_name_plural = _('Требования к кандидатам')
        

        
class Salary(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))
    currency = models.CharField(max_length=5, verbose_name=_('Валюта'), choices=CURRENCY_CHOICES)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['amount', 'currency'], name='unique_amount_currency')
        ]
    
    def __str__(self) -> str:
        return f'{self.amount} {self.currency}'
    
    @property
    def symbol(self) -> str:
        return CURRENCY_SYMBOLS.get(self.currency, self.currency)


class HourlyPaymentOption(models.Model):
    payment_type = models.CharField(max_length=100, verbose_name=_('Тип оплаты (для студентов, ночные, испытательный и тд.)'))
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'), default=Decimal(5))

    def __str__(self):
        if self.hourly_rate:
            return f"{self.payment_type}: {self.hourly_rate}/h"
        return f"{self.payment_type}"

    class Meta:
        verbose_name = _('Вариант почасовой оплаты')
        verbose_name_plural = _('Варианты почасовой оплаты')

class View(models.Model):
    ip = models.CharField(max_length=64, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    region_name = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    isp = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.BooleanField(blank=True, null=True)

class Vacancy(models.Model):
    name = models.CharField(verbose_name=_('Название вакансии'), max_length=300)
    title = models.CharField(verbose_name=_('Заголовок вакансии'), max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("Место работы"))
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_("Регион"))
    card_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name=_("Картинка карточки вакансии и обложки"), related_name='vacancy_card_photo')
    photos = models.ManyToManyField(Photo, verbose_name=_('Фотографии вакансии'))
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name=_('Видеозапись вакансии'), null=True, blank=True)
    info_label = models.ForeignKey(InfoLabel, on_delete=models.SET_NULL, verbose_name=_("Описание стандарт"), null=True, blank=True)
    salary_per_hour = models.ManyToManyField(HourlyPaymentOption, verbose_name=_("Варианты почасовой оплаты"), blank=True)
    salary_per_mounth_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка месячная минимум', null=True, blank=True)
    salary_per_mounth_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка месячная максимум', null=True, blank=True)
    salary_per_mounth_fixed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка месячная фиксированая (если нет минимума или максимума)', null=True, blank=True)
    salary_per_hour_fixed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка почасовая (если нет месячной)', null=True, blank=True)
    default_currency = models.CharField(max_length=5, verbose_name=_('Валюта по умолчанию'), choices=CURRENCY_CHOICES, default="PLN")
    salary_is_netto = models.BooleanField(verbose_name=_('Зарплата netto?'), default=True)
    work_duties = models.ManyToManyField(WorkDuty, verbose_name=_('Обязанности по работе'), blank=True)
    requirements = models.ManyToManyField(Requirement, verbose_name=_('Требования к кандидату'), blank=True)
    work_schedule = models.TextField(verbose_name=_('График работы'), blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    date_time_update = models.DateTimeField(auto_now=True, verbose_name=_('Дата изменения'))
    sex = models.ManyToManyField(Sex, verbose_name=_('Пол'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Категория"))
    index = models.ForeignKey(Index, on_delete=models.CASCADE, verbose_name=_("Индекс (служебное)"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Активно'), default=True)
    irrelevant = models.BooleanField(verbose_name=_('Не актуально'), default=False)
    with_experience = models.BooleanField(verbose_name=_('C опытом работы'), default=False)
    views = models.ManyToManyField(View, blank=True)
    
    @property
    def symbol(self):
        return CURRENCY_SYMBOLS.get(self.default_currency, self.default_currency)
    
    
    def _get_salary_text(self, is_netto_text):
        from_text = _('от')
        to_text = _('до')
        if self.salary_per_mounth_fixed is not None:
            return f"{self.salary_per_mounth_fixed} {self.symbol}"
        elif self.salary_per_mounth_min is not None and self.salary_per_mounth_max is not None:
            return f"{self.salary_per_mounth_min} - {self.salary_per_mounth_max} {self.symbol}"
        elif self.salary_per_mounth_min is not None:
            return f"{from_text} {self.salary_per_mounth_min} {self.symbol}"
        elif self.salary_per_mounth_max is not None:
            return f"{to_text} {self.salary_per_mounth_max} {self.symbol}"
        elif self.salary_per_hour_fixed:
            return f"{self.salary_per_hour_fixed} {self.symbol}/h {is_netto_text}"
        else:
            return ""
    
    def get_salary_text_for_vacancy_list(self):
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

    embeded.short_description = _('Встройка в YouTube')

    class Meta:
        ordering = ['name']
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')