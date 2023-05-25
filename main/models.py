from django.db import models
from tinymce import models as tinymce_models

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

class Vacancy(models.Model):
	name = models.CharField(verbose_name='Название', max_length=300)
	city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
	price = models.FloatField(verbose_name='Ставка(zlot)')
	sex = models.ManyToManyField(Sex, verbose_name='Пол')
	text = tinymce_models.HTMLField()

	def __str__(self):
		return '{} | {}'.format(self.name, self.city)

	class Meta:
		verbose_name = 'Вакансия'
		verbose_name_plural = 'Вакансии'