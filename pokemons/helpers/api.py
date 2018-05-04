import requests

from pokemons.helpers.pokemon import get_pokemon_attributes
from pokemons.models import Pokemon


def _pokemon_existent(pokemon_name):
    return Pokemon.objects.filter(name=pokemon_name).exists()


def _save_pokemon_from_api(pokemon_url):
    response = requests.get(pokemon_url).json()
    attributes = get_pokemon_attributes(response)
    new_pokemon = Pokemon(
        id=response['id'],
        name=response['name'],
        sprite=response['sprites']['front_default'],
        defense=attributes['defense'],
        attack=attributes['attack'],
        hp=attributes['hp']
    )
    new_pokemon.save()


def bulk_save_pokemon_from_api():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=802')
    if not response.ok:
        return
    response = response.json()
    for pokemon in response['results']:
        if not _pokemon_existent(pokemon.name):
            _save_pokemon_from_api(pokemon['url'])
