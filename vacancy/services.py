import requests
from .models import City, State, Photo, Video, InfoLabel, HourlyPaymentOption, WorkDuty, Requirement, Sex, Category, Index, Vacancy
from django.db import transaction, models
from django.conf import settings

def get_or_create_related_object(model, data):
    obj, created = model.objects.get_or_create(**data)
    return obj

def update_or_create_related_object(model: models.Model, data):
    id = data.pop('id')
    qs = model.objects.filter(**data)
    if qs.count() > 1:
        return qs.last()
    obj, created = model.objects.update_or_create(**data)
    return obj

#тут косячище, треба зробити щоб не оновлювалися ідшники, для кожного обєкту походу треба написати свій апдейтер
@transaction.atomic
def create_or_update_vacancies_from_json(data, source):
    for vacancy_data in data:
        obj_id = vacancy_data.pop('id')
        city_data = vacancy_data.pop('city')
        state_data = vacancy_data.pop('state')
        card_photo_data = vacancy_data.pop('card_photo')
        photos_data = vacancy_data.pop('photos')
        video_data = vacancy_data.pop('video', None)
        info_label_data = vacancy_data.pop('info_label', None)
        salary_per_hour_data = vacancy_data.pop('salary_per_hour')
        work_duties_data = vacancy_data.pop('work_duties')
        requirements_data = vacancy_data.pop('requirements')
        sex_data = vacancy_data.pop('sex')
        category_data = vacancy_data.pop('category')
        index_data = vacancy_data.pop('index', None)
        views = vacancy_data.pop('views')
        vacancy_data['sync_id'] = f'{obj_id}-{source}'

        city = update_or_create_related_object(City, city_data)
        state = update_or_create_related_object(State, state_data)
        if not Vacancy.objects.filter(sync_id=vacancy_data['sync_id']).exists():
            card_photo = Photo.objects.first()
            photos = Photo.objects.all()[:5]
            video = None
        info_label = update_or_create_related_object(InfoLabel, info_label_data) if info_label_data else None
        salary_per_hour = [update_or_create_related_object(HourlyPaymentOption, option) for option in salary_per_hour_data]
        work_duties = [update_or_create_related_object(WorkDuty, duty) for duty in work_duties_data]
        requirements = [update_or_create_related_object(Requirement, requirement) for requirement in requirements_data]
        sex = [update_or_create_related_object(Sex, s) for s in sex_data]
        category = update_or_create_related_object(Category, category_data)
        index = update_or_create_related_object(Index, index_data) if index_data else None

        vacancy_data['city'] = city
        vacancy_data['state'] = state
        vacancy_data['card_photo'] = card_photo
        vacancy_data['video'] = video
        vacancy_data['info_label'] = info_label
        vacancy_data['category'] = category
        vacancy_data['index'] = index
        vacancy_data['source'] = source
        

        vacancy, created = Vacancy.objects.update_or_create(
            sync_id=vacancy_data['sync_id'],
            defaults=vacancy_data
        )
        vacancy.photos.set(photos)
        vacancy.salary_per_hour.set(salary_per_hour)
        vacancy.work_duties.set(work_duties)
        vacancy.requirements.set(requirements)
        vacancy.sex.set(sex)
        vacancy.save()
        

def refresh_data_from_sources():
    sources: str = settings.DATA_SOURCES
    sources = sources.split(',')
    API_ENDPOINT = '/vacancy/api/list/'
    for source in sources:
        response = requests.get(source+API_ENDPOINT)
        if response.status_code == 200:
            create_or_update_vacancies_from_json(source=source, data=response.json())