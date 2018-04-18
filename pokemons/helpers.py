import json

from django.conf import settings

import requests as r

from pokemons.models import Pokemon


def init_pokemon_object(pid):
    if not Pokemon.objects.filter(id=pid).exists():
        pokemon_dict = r.get(
            '{pokeapi}/{pokemon_id}'.format(
                pokeapi=settings.POKEAPI_POKEMON_URL,
                pokemon_id=pid
            )
        )
        pokemon_dict = json.loads(pokemon_dict.text)
        attributes = get_pokemon_attributes(pokemon_dict)
        new_pokemon = Pokemon(
            id=pid,
            name=pokemon_dict['name'],
            sprite=pokemon_dict['sprites']['front_default'],
            defense=attributes['defense'],
            attack=attributes['attack'],
            hp=attributes['hp']
        )
        return new_pokemon
    return Pokemon.objects.get(id=pid)


def get_pokemon_attributes(pokemon_dict):
    stats = [(stats['stat']['name'], stats['base_stat'])
             for stats in pokemon_dict['stats']]
    stats_dict = {}
    for stat in stats:
        stat_name = stat[0]
        stat_value = stat[1]
        if (stat_name == 'defense' or
            stat_name == 'attack' or
                stat_name == 'hp'):
            stats_dict[stat_name] = stat_value
    return stats_dict


def check_if_pokemon_stats_exceeds_600(pokemon_list):
    stats = [pokemon.attack + pokemon.defense + pokemon.hp
             for pokemon in pokemon_list]
    result = sum(stats)
    return result >= 600
