import json

from django.conf import settings
from django.test import TestCase

import requests
from model_mommy import mommy

from common.utils.tests import TestCaseUtils
from pokemons.helpers import (
    check_if_pokemon_stats_exceeds_600, get_pokemon_attributes, init_pokemon_object
)
from pokemons.models import Pokemon


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

    def example_request(self):
        return requests.get(
            '{pokeapi}/pokemon/{pokemon_id}'.format(
                pokeapi=settings.POKEAPI_URL,
                pokemon_id=self.creator_pokemon.id
            )
        )

    def test_function_returns_a_pokemon_if_existent(self):
        pokemon = init_pokemon_object(self.creator_pokemon.id)
        self.assertIsInstance(pokemon, Pokemon)

    def test_function_returns_a_pokemon_if_non_existent(self):
        pokemon = init_pokemon_object(15)
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

    def test_request_response_is_a_dict(self):
        response = self.example_request()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_pokemon_attributes_is_a_valid_dict(self):
        response = json.loads(self.example_request().text)
        attributes_dict = get_pokemon_attributes(response)
        expected_dict = dict(
            defense=58,
            attack=64,
            hp=58
        )
        self.assertDictEqual(expected_dict, attributes_dict)

    def test_pokemon_with_stats_higher_than_600_is_invalid(self):
        for pokemon in self.pokemon_list:
            pokemon.attack = 80
            pokemon.defense = 80
            pokemon.hp = 80
            pokemon.save()
        stats = check_if_pokemon_stats_exceeds_600(self.pokemon_list)
        self.assertTrue(stats)
