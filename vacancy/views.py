import datetime
import json
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
import requests
from .models import Sex, Vacancy, Category, State, View
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from rest_framework import generics
from .models import Vacancy
from .serializers import VacancySerializer

def get_user_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return forwarded_for.split(',')[-1].strip() if forwarded_for else request.META.get('REMOTE_ADDR')

def send_telegram(message: str, uploaded_file=None, TOKEN=settings.TELEGRAM_TOKEN, CHAT_ID=settings.TELEGRAM_CHAT):
    
    api = 'https://api.telegram.org/bot'
    
    # Проверяем, есть ли файл
    if uploaded_file:
        method = api + TOKEN + '/sendDocument'
        params = {
            'chat_id': CHAT_ID,
            'caption': message,  # Текстовое описание файла
            'parse_mode': 'HTML'
        }
        files = {'document': (uploaded_file.name, uploaded_file)}
        response = requests.post(method, params=params, files=files)
    else:
        method = api + TOKEN + '/sendMessage'
        params = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(method, data=params)

    if response.status_code != 200:
        print(response.text)

# Create your views here.
class VacancyListView(ListView):
    def get(self, request: HttpRequest): 
        vacancies = Vacancy.objects.filter(active=True)
        categories = Category.objects.all()
        states = State.objects.all()
        sexes = Sex.objects.all()
        if request.GET.get('clear', '0') != '1':
            selected_categories = list(map(int, request.GET.getlist('profession', [])))
            selected_irrelevants = list(map(int, request.GET.getlist('irrelevant', [])))
            selected_with_experience = list(map(int, request.GET.getlist('with_experience', [])))
            selected_sexes = list(map(int, request.GET.getlist('sex', [])))
            selected_states = list(map(int, request.GET.getlist('location', [])))
        else:
            selected_categories, selected_sexes, selected_states, selected_irrelevants, selected_with_experience = ([], [], [], [], [])

        if len(selected_irrelevants) > 0:
            if selected_irrelevants[0] != 2:
                vacancies = vacancies.filter(irrelevant=False if selected_irrelevants[0] == 1 else True)
                
        if len(selected_with_experience) > 0:
            vacancies = vacancies.filter(with_experience=False if selected_with_experience[0] == 2 else True)
        
        if len(selected_categories) > 0:
            vacancies = vacancies.filter(category__id__in=selected_categories)
            
        if len(selected_sexes) > 0:
            vacancies = vacancies.filter(sex__id__in=selected_sexes)
        
        if len(selected_states) > 0:
            vacancies = vacancies.filter(state__id__in=selected_states)
            
        
                
            
        # send_mail('Тест', f'{vacancies.values_list("id", "category")}', 'invilsomail@gmail.com', ['invilsomail@gmail.com'])
        vacancies = vacancies.order_by('date_time')
        vacancies = vacancies.order_by('irrelevant')
        context = {
            'vacancies': vacancies,
            'vacancies_len': vacancies.count(),
            'categories': categories, 
            'states': states, 
            'sexes': sexes,
            'selected_categories': selected_categories,
            'selected_sexes': selected_sexes,
            'selected_states': selected_states,
            'selected_irrelevants': selected_irrelevants,
            'selected_with_experience': selected_with_experience,
            'selected_nav_name': 'vacancies'
        }
        return render(request, 'vacancy/list.html', context)
    
class VacancyView(ListView):
    def get(self, request, pk): 
        vacancy = Vacancy.objects.get(pk=pk)
        
        last_day_views = vacancy.views.filter(
            date_time__gte=timezone.now() - datetime.timedelta(hours=24),
        )
        # Проверяем, просматривалась ли вакансия ранее
        user_ip = get_user_ip(request)
        if not last_day_views.filter(ip = user_ip).exists():
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
        return render(request, 'vacancy/item.html', {'vacancy':vacancy, 'selected_nav_name': 'vacancies'})
    
    
def send_mail(subject, message, uploaded_file):
    from_email = settings.EMAIL_HOST_USER  # Замените на свой адрес электронной почты
    recipient_list = [settings.FORN_SEND_MAIL]  # Список адресов получателей
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
        attachments=[(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)] if uploaded_file else None
    )
    email.send()
    
    
class ApplyToVacancyView(ListView):
    def post(self, request: HttpRequest): 
        name = request.POST.get('name', 'Неизвестный').strip().title()
        vacancy_info = request.POST.get('vacancy', '').strip()
        phone = request.POST.get('phone', 'Не указанно').strip()
        uploaded_file = request.FILES.get('file')
        v_id = request.POST.get('v_id', '')
        want_partner = request.POST.get('want_partner', '')
        
        if name == '' or name == 'Неизвестный':
            return redirect(request.META['HTTP_REFERER'])
            
        if phone == '' or phone == 'Не указанно':
            return redirect(request.META['HTTP_REFERER'])
            
        if vacancy_info == '':
            if v_id != '':
                v_id = int(v_id)
                vacancy = Vacancy.objects.get(id=v_id)
                vacancy_info = vacancy.category
            else:
                vacancy_info = 'Вакансия не указана'
                
        if want_partner == '':      
            if v_id != '':    
                subject = f"Отклик на вакансию от {name}"
                message = f"Пользователь {name} подал заявку на вакансию:\n\n{vacancy_info}\n\nТелефон: {phone}"
            else:
                subject = f"Запрос на обратную связь от {name}"
                message = f"Пользователь {name} подал заявку на обратную связь:\n\n{vacancy_info}\n\nТелефон: {phone}"
        else:
            subject = f"Запрос на становление партнером от {name}"
            message = f"Пользователь {name} подал заявку на то чтобы стать партнером:\n\n{vacancy_info}\n\nТелефон: {phone}"
            
        
        
        if settings.FORM_SEND_TYPE == 'email':
            send_mail(subject, message, uploaded_file)
        elif settings.FORM_SEND_TYPE == 'tg':
            if want_partner != '': 
                send_telegram(f'<b>{subject}</b>\n\n{message}', uploaded_file, CHAT_ID=settings.PARTNER_CHATID_TG)
            else:
                send_telegram(f'<b>{subject}</b>\n\n{message}', uploaded_file)
        elif settings.FORM_SEND_TYPE == 'email/tg':
            send_mail(subject, message, uploaded_file)
            send_telegram(f'<b>{subject}</b>\n\n{message}', uploaded_file)
            
            
        return redirect(request.META['HTTP_REFERER'])

class VacancyListViewAPI(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
