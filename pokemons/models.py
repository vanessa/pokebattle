from django.db import models
from battles.variables import POKEAPI_URL, POKEMON_URL
import requests as r
import json
# import pokebase as pb


class Pokemon(models.Model):
    id = models.SmallIntegerField('Pokemon\'s ID', primary_key=True)
    name = models.CharField('Pokemon\'s name', max_length=60)

    """ Attributes """
    attack = models.SmallIntegerField('Attack')
    defense = models.SmallIntegerField('Defense')
    hp = models.SmallIntegerField('HP')

    # TO-DO: Remove this as soon as possible, not reliable
    def get_picture(self):
        pokemon = r.get(
            POKEMON_URL + str(self.id)
            )
        pokemon = json.loads(pokemon.text)
        return pokemon['sprites']['front_default']

    def __str__(self):
        return self.name
