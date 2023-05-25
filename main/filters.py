import django_filters
from .models import *
from django import forms

sex_list = (('М', 'Мужчина'), ('Ж', 'Женщина'))

class VacancyFilter(django_filters.FilterSet):
	price = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control'}))
	class Meta:
		model = Vacancy
		fields = ['city', 'sex']