from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pracabaza.settings")
django.setup()

from vacancy.models import Vacancy, HourlyPaymentOption
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

def get_obj_from_list(data: list, id: int) -> dict:
    for item in data:
        if item.get('pk') == id:
            return item.get('fields')
        
def load_json(file_path: str) -> list:
    with open(file_path) as f:
        return json.load(f)
    
vacancies_json = load_json(Path('backups', '02_04', 'vacancy_vacancys.json'))
salaries_json = load_json(Path('backups', '02_04', 'vacancy_salarys.json'))
hps_json = load_json(Path('backups', '02_04', 'vacancy_hourlypaymentoptions.json'))
with transaction.atomic():
    for vacancy in HourlyPaymentOption.objects.all():
        vacancy_json = get_obj_from_list(hps_json, vacancy.pk)
        amount = Decimal(get_obj_from_list(salaries_json, vacancy_json.get('hourly_rates', [1])[0]).get('amount', 1))
        vacancy.hourly_rate = amount
        vacancy.save()
                
    for vacancy in Vacancy.objects.all():
        vacancy_json = get_obj_from_list(vacancies_json, vacancy.pk)
        fields = ['salary_per_hour_fixed', 'salary_per_mounth_fixed', 'salary_per_mounth_max', 'salary_per_mounth_min']
        for field in fields:
            try:
                amount = Decimal(get_obj_from_list(salaries_json, vacancy_json.get(field, [1])[0]).get('amount', 1))
                setattr(vacancy, field, amount)
            except Exception as e:
                print(e)
        vacancy.save()
