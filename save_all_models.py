from datetime import datetime
from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pracabaza.settings")
django.setup()


from django.core.serializers import serialize
from vacancy.models import HourlyPaymentOption, Requirement, WorkDuty, Video, Photo, Index, Category, InfoLabel, Sex, City, State, Salary, Vacancy, View
from info_pages.models import Photo as PhotoInfo, PhoneNumber, SocialNetwork, ContactInfo, AboutUs, Guarantees, Partners, Team, LegalDocument
from django.apps import apps

directory = Path('backups', datetime.today().strftime('%d_%m'))
os.makedirs(directory, exist_ok=True)
app_names = ['vacancy', 'info_pages']

def extract_and_save_to_json(model_class, file_name):
    instances = model_class.objects.all()
    json_data = serialize('json', instances)
    with open(Path(directory, file_name), 'w') as json_file:
        json_file.write(json_data)

for app_name in app_names:
    app_config = apps.get_app_config(app_name)
    for model in app_config.get_models():
        extract_and_save_to_json(model, f'{app_name}_{model.__name__.lower()}s.json')
# Пример вызова функции для каждой модели
# 
# extract_and_save_to_json(Requirement, 'requirements.json')
# extract_and_save_to_json(WorkDuty, 'work_duties.json')
# extract_and_save_to_json(Video, 'videos.json')
# extract_and_save_to_json(Photo, 'photos.json')
# extract_and_save_to_json(Index, 'indexes.json')
# extract_and_save_to_json(Category, 'categories.json')
# extract_and_save_to_json(InfoLabel, 'info_labels.json')
# extract_and_save_to_json(Sex, 'sexes.json')
# extract_and_save_to_json(City, 'cities.json')
# extract_and_save_to_json(State, 'states.json')
# extract_and_save_to_json(PhotoInfo, 'photo_infos.json')
# extract_and_save_to_json(PhoneNumber, 'phone_numbers.json')
# extract_and_save_to_json(SocialNetwork, 'social_networks.json')
# extract_and_save_to_json(ContactInfo, 'contact_infos.json')
# extract_and_save_to_json(AboutUs, 'about_us.json')
# extract_and_save_to_json(Guarantees, 'guarantees.json')
# extract_and_save_to_json(Partners, 'partners.json')
# extract_and_save_to_json(Team, 'team.json')
# extract_and_save_to_json(Salary, 'salaries.json')
# extract_and_save_to_json(Vacancy, 'vacancies.json')
# extract_and_save_to_json(View, 'views.json')
# extract_and_save_to_json(LegalDocument, 'legal_documents.json')