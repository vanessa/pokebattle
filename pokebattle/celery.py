# coding: utf-8
# pylint: skip-file

from __future__ import absolute_import

import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab
from decouple import config


settings_module = config("DJANGO_SETTINGS_MODULE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery('pokebattle')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'save_pokemon_from_the_api': {
        'schedule': crontab(hour=10, minute=0, day_of_week='monday'),
        'task': 'pokemons.tasks.save_all_pokemon_from_api'
    }
}
