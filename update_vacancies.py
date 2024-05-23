from decimal import Decimal
import json
import os
from pathlib import Path
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pracabaza.settings")
django.setup()

from vacancy.services import refresh_data_from_sources
refresh_data_from_sources()