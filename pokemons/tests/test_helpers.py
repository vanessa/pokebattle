from django.conf import settings
from django.test import TestCase

import requests
import responses
from model_mommy import mommy

from common.utils.tests import TestCaseUtils
from pokemons.helpers.api_wrapper import bulk_save_pokemon_from_api
from pokemons.helpers.pokemon import (
    get_pokemon_attributes, init_pokemon, pokemon_stats_exceeds_limit
)
from pokemons.models import Pokemon
from pokemons.tests.mocks import (
    POKEAPI_POKEMON_DATA_EXAMPLE_FIRST, POKEAPI_POKEMON_DATA_EXAMPLE_SECOND,
    POKEAPI_POKEMON_LIST_EXAMPLE
)


class TestPokemonHelpers(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.creator_pokemon = mommy.make(
            'pokemons.Pokemon', name='Creatorpokemon', id=5)
        self.opponent_pokemon = mommy.make(
            'pokemons.Pokemon', name='Opponentpokemon')
        self.pokemon_list = mommy.make(
            'pokemons.Pokemon', _quantity=3
        )

    def test_function_returns_a_pokemon_if_existent(self):
        pokemon = init_pokemon(self.creator_pokemon.id)
        self.assertIsInstance(pokemon, Pokemon)

    def test_pokeapi_url_is_correct(self):
        url = settings.POKEAPI_URL
        self.assertEqual(url, 'http://pokeapi.co/api/v2')

    def test_pokemon_id_is_within_the_api_constraints(self):
        self.creator_pokemon.id = 4
        self.creator_pokemon.save()
        is_within_limit = 1 <= self.creator_pokemon.id <= 802
        self.assertTrue(is_within_limit)

    def test_pokemon_id_outside_api_constraints_breaks(self):
        self.creator_pokemon.id = 5000
        self.creator_pokemon.save()
        is_within_limit = 1 <= self.creator_pokemon.id <= 802
        self.assertFalse(is_within_limit)

    @responses.activate
    def test_request_response_is_a_dict(self):
        url = '{pokeapi}/pokemon/{pokemon_id}'.format(
            pokeapi=settings.POKEAPI_URL,
            pokemon_id=self.creator_pokemon.id
        )
        responses.add(responses.GET, url, status=200, headers={'Content-Type': 'application/json'})
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    @responses.activate
    def test_pokemon_attributes_is_a_valid_dict(self):
        url = '{pokeapi}/pokemon/{pokemon_id}'.format(
            pokeapi=settings.POKEAPI_URL,
            pokemon_id=self.creator_pokemon.id
        )
        responses.add(responses.GET, url, status=200, headers={'Content-Type': 'application/json'},
                      json=POKEAPI_POKEMON_DATA_EXAMPLE_FIRST)
        response = requests.get(url).json()
        attributes_dict = get_pokemon_attributes(response)
        expected_dict = dict(
            defense=30,
            attack=60,
            hp=40
        )
        self.assertDictEqual(expected_dict, attributes_dict)

    def test_pokemon_with_stats_higher_than_limit_is_invalid(self):
        for pokemon in self.pokemon_list:
            pokemon.attack = 80
            pokemon.defense = 80
            pokemon.hp = 80
            pokemon.save()
        stats = pokemon_stats_exceeds_limit(self.pokemon_list)
        self.assertTrue(stats)


class TestAPIHelpers(TestCase):

    @responses.activate
    def test_access_api_helper_saves_pokemon(self):
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/?limit=802',
            status=200, json=POKEAPI_POKEMON_LIST_EXAMPLE)
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/21/',
            status=200, json=POKEAPI_POKEMON_DATA_EXAMPLE_FIRST)
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/22/',
            status=200, json=POKEAPI_POKEMON_DATA_EXAMPLE_SECOND)
        bulk_save_pokemon_from_api()
        pokemon_count = Pokemon.objects.count()
        self.assertEqual(pokemon_count, 2)

    @responses.activate
    def test_access_api_helper_doesnt_save_duplicate(self):
        mommy.make('pokemons.Pokemon', name='fearow')
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/?limit=802',
            status=200, json=POKEAPI_POKEMON_LIST_EXAMPLE)
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/21/',
            status=200, json=POKEAPI_POKEMON_DATA_EXAMPLE_FIRST)
        responses.add(
            responses.GET, 'https://pokeapi.co/api/v2/pokemon/22/',
            status=200, json=POKEAPI_POKEMON_DATA_EXAMPLE_SECOND)
        bulk_save_pokemon_from_api()
        pokemon_count = Pokemon.objects.count()
        self.assertEqual(pokemon_count, 2)
