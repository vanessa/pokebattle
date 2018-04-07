import json

import requests as r

from pokemons.models import Pokemon

from .variables import POKEMON_URL


def create_pokemon_if_not_exists(pid):
    try:
        Pokemon.objects.get(id=pid)
    except Pokemon.DoesNotExist:
        pkn = r.get(
            POKEMON_URL + str(pid)
        )
        pkn = json.loads(pkn.text)
        new_pokemon = Pokemon(
            id=pid,
            name=pkn['name'],
            sprite=pkn['sprites']['front_default']
        )
        stats = [(stats['stat']['name'], stats['base_stat'])
                 for stats in pkn['stats']]
        stats_list = {}
        for stat in stats:
            stat_name = stat[0]
            stat_value = stat[1]
            if (stat_name == 'defense' or
                stat_name == 'attack' or
                    stat_name == 'hp'):
                stats_list[stat_name] = stat_value
        new_pokemon.defense = stats_list['defense']
        new_pokemon.attack = stats_list['attack']
        new_pokemon.hp = stats_list['hp']
        new_pokemon.save()


def check_if_pokemon_stats_exceeds_600():
    pass
