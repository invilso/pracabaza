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
	name = models.CharField(verbose_name='Пол', max_length=100)

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
	name = models.CharField(verbose_name='Название', max_length=300)

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

class Vacancy(models.Model):
	name = models.CharField(verbose_name='Название', max_length=300)
	state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Регион")
	city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)	
	price = models.FloatField(verbose_name='Ставка(zlot)')
	sex = models.ManyToManyField(Sex, verbose_name='Пол')
	text = tinymce_models.HTMLField()
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
	index = models.ForeignKey(Index, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Индекс")

	def __str__(self):
		return f'{self.index} - {self.name} | {self.city}'

	class Meta:
		ordering = ['name']
		verbose_name = 'Вакансия'
		verbose_name_plural = 'Вакансии'