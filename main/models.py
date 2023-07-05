from django.db import models
from tinymce import models as tinymce_models

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
		verbose_name_plural = 'Список городов'

class Sex(models.Model):
	name = models.CharField(verbose_name='Пол', max_length=100, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Пол'
		verbose_name_plural = 'Пол'
  
class InfoLabels(models.Model):
	text = tinymce_models.HTMLField(null=True, blank=True)

	def __str__(self):
		return self.text

	class Meta:
		verbose_name = 'Информационная табличка'
		verbose_name_plural = 'Информационные таблички'
  
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

class View(models.Model):
    ip = models.CharField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    country = models.CharField(null=True, blank=True)
    region_name = models.CharField(null=True, blank=True)
    city = models.CharField(null=True, blank=True)
    isp = models.CharField(null=True, blank=True)
    mobile = models.BooleanField(blank=True, null=True)

class Vacancy(models.Model):
	name = models.CharField(verbose_name='Название', max_length=300)
	city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Место работы")
	state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="Регион")
	price = models.FloatField(verbose_name='Ставка(zlot)')
	sex = models.ManyToManyField(Sex, verbose_name='Пол')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
	index = models.ForeignKey(Index, on_delete=models.CASCADE, verbose_name="Индекс")
	text = tinymce_models.HTMLField()
	active = models.BooleanField(verbose_name='Активно', default=True)
	views = models.ManyToManyField(View)

	def __str__(self):
		return f'{self.index} - {self.name} | {self.city}'

	class Meta:
		ordering = ['name']
		verbose_name = 'Вакансия'
		verbose_name_plural = 'Вакансии'