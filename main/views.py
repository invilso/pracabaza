from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

def ListView(request):
	items = Vacancy.objects.order_by('-id')
	cities = City.objects.all().order_by('name')
	sexes = Sex.objects.all()
	labels = InfoLabels.objects.all()
	categoryes = Category.objects.all().order_by('name')
	states = State.objects.all().order_by('name')

	if request.method == 'GET':
		action = request.GET.get('clear')
		if action == "true":
			request.GET = {}

		city = request.GET.get('city')
		if city:
			items = items.filter(city__pk=city)

		category = request.GET.get('category')
		if category:
			items = items.filter(category__pk=category)
   
		state = request.GET.get('state')
		if state:
			items = items.filter(state__pk=state)
		
		sex = request.GET.get('sex')
		if sex:
			items = items.filter(sex__pk=sex)

		answer = request.GET.get('order')
		if answer == "1":
			items = items.order_by('-price')
		elif answer == "2":
			items = items.order_by('price')

	
	context = {
		'items':items,
		'cities':cities,
		'sexes':sexes,
		'labels':labels,
		'categoryes':categoryes,
		'states': states
	}

	return render(request, 'main/list.html', context)

def ItemView(request, id):
	context = {
		'item':Vacancy.objects.get(id=id),
	}

	return render(request, 'main/item.html', context)