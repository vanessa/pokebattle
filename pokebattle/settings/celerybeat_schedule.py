from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'save_pokemon_from_the_api': {
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
        'task': 'pokemons.tasks.save_all_pokemon_from_api'
    }
}

