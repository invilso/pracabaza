from datetime import date, timedelta, datetime
import json
from random import randint
import random
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from .models import *
import plotly.graph_objects as go
from plotly.offline import plot
import requests

def get_user_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return forwarded_for.split(',')[-1].strip() if forwarded_for else request.META.get('REMOTE_ADDR')

def ListView(request):
    items = Vacancy.objects.filter(active=True).order_by('-id')
    cities = City.objects.all().order_by('name')
    sexes = Sex.objects.all()
    labels = InfoLabels.objects.all()
    categoryes = Category.objects.annotate(total_vacancies=Count('vacancy')).order_by('name')
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

def create_view(request):
    cities = City.objects.all().order_by('name')
    sexes = Sex.objects.all()
    labels = InfoLabels.objects.all()
    categoryes = Category.objects.annotate(total_vacancies=Count('vacancy')).order_by('name')
    states = State.objects.all().order_by('name')
    indexes = Index.objects.all().order_by('name')
    context = {
        'cities':cities,
        'sexes':sexes,
        'labels':labels,
        'categoryes':categoryes,
        'indexes' : indexes,
        'states': states
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        city_name = request.POST.get('city')
        state_name = request.POST.get('state')
        price = request.POST.get('price')
        sex_names = request.POST.getlist('sex')
        category_name = request.POST.get('category')
        index_name = request.POST.get('index')
        text = request.POST.get('text')
        active = request.POST.get('active', True)

        city, _ = City.objects.get_or_create(name=city_name)
        state, _ = State.objects.get_or_create(name=state_name)
        category, _ = Category.objects.get_or_create(name=category_name)
        index, _ = Index.objects.get_or_create(name=index_name)

        vacancy = Vacancy(
            name=name,
            city=city,
            state=state,
            category=category,
            index=index,
            price=float(price),
            text=text,
            active=active,
        )
        vacancy.save()
        vacancy.sex.set(Sex.objects.filter(name__in=sex_names))
        vacancy.save()

        return redirect('main:list')

    return render(request, 'main/create.html', context)

def ItemView(request, id):
    vacancy = Vacancy.objects.get(id=id)
    context = {
        'item': vacancy,
    }
 
    # Проверяем, была ли установлена сессия для данного пользователя
    if 'viewed_vacancies' not in request.session:
        request.session['viewed_vacancies'] = []
    
    # Проверяем, просматривалась ли вакансия ранее
    if id not in request.session['viewed_vacancies']:
        user_ip = get_user_ip(request)
        if user_ip != '127.0.0.1':
            resp = requests.get(f'http://ip-api.com/json/{user_ip}?fields=status,message,country,regionName,city,isp,mobile,query').text
            data: dict = json.loads(resp)
        else:
            data: dict = {}
        view = View(
            ip=user_ip,
            country = data.get('country'),
            region_name = data.get('regionName'),
            city = data.get('city'),
            isp = data.get('isp'),
            mobile = data.get('mobile'),
            )
        view.save()
        vacancy.views.add(view)
        vacancy.save()
        
        # Добавляем идентификатор вакансии в список просмотренных в сессии
        request.session['viewed_vacancies'].append(id)

    return render(request, 'main/item.html', context)

def plot_graph(request, id):
    if not request.user.is_authenticated:
        return redirect('main:list')
    end_date = date.today()  # Текущая дата
    start_date = end_date - timedelta(days=30)  # Дата 30 дней назад
    
    # Агрегация просмотров по дате
    vacancy = Vacancy.objects.get(id=id)
    views_by_date = vacancy.views.all().filter(date__range=(start_date, end_date)).values('date').annotate(view_count=Count('id')).order_by('date')

    # Извлечение данных просмотров
    date_list = [view['date'] for view in views_by_date]
    view_count_list = [view['view_count'] for view in views_by_date]

    # Создание графика
    fig = go.Figure(data=go.Scatter(x=date_list, y=view_count_list, mode='lines+markers'))

    fig.update_layout(
        title='График просмотров по дате (за последние 30 дней)',
        xaxis_title='Дата',
        yaxis_title='Просмотры',
    )

    plot_div = fig.to_html(full_html=False, default_height=500)
    return render(request, 'main/graph.html', {'plot_div': plot_div})