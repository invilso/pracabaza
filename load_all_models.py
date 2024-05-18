from datetime import datetime
from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrow_rsc.settings")
django.setup()

from django.core.management import call_command

directory = Path('backups', datetime.today().strftime('%d_%m'))

json_files = os.listdir(directory)
json_files = [
    'vacancy_salarys.json',
    'vacancy_views.json',
    'vacancy_hourlypaymentoptions.json',
    'vacancy_requirements.json',
    'vacancy_workdutys.json',
    'vacancy_videos.json',
    'vacancy_photos.json',
    'vacancy_indexs.json',
    'vacancy_categorys.json',
    'vacancy_infolabels.json',
    'vacancy_sexs.json',
    'vacancy_citys.json',
    'vacancy_states.json',
    'vacancy_vacancys.json',
    'info_pages_photos.json',
    'info_pages_phonenumbers.json',
    'info_pages_socialnetworks.json',
    'info_pages_contactinfos.json',
    'info_pages_aboutuss.json',
    'info_pages_guaranteess.json',
    'info_pages_partnerss.json',
    'info_pages_teams.json',
    'info_pages_legaldocuments.json'
]
for json_file in json_files:
    call_command('loaddata', Path(directory, json_file))