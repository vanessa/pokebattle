import logging

from pokebattle import celery_app
from pokemons.helpers.api import bulk_save_pokemon_from_api


@celery_app.task
def save_all_pokemon_from_api():
    logging.info('save pokemon from api')
    bulk_save_pokemon_from_api()
