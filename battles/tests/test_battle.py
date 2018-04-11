from django.test import TestCase

from model_mommy import mommy

from battles.helpers import compare_two_pokemons
from common.utils.tests import TestCaseUtils


class TestBattle(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.creator_pokemon = mommy.make(
            'pokemons.Pokemon', name='Creatorpokemon', attack=60, defense=40, hp=30)
        self.opponent_pokemon = mommy.make(
            'pokemons.Pokemon', name='Opponentpokemon', attack=30, defense=50, hp=10)

    def test_two_pokemon_comparison(self):
        winner = compare_two_pokemons(
            self.creator_pokemon.id, self.opponent_pokemon.id)
        self.assertEqual(winner, self.creator_pokemon)
