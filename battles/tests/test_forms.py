from django.test import TestCase

from model_mommy import mommy

from battles.forms import ChooseTeamForm, CreateBattleForm
from common.utils.tests import TestCaseUtils


class TestCreateBattleForm(TestCaseUtils, TestCase):

    def test_battle_empty_opponent(self):
        params = {
            'initial': {
                'creator': self.user.id
            },
            'data': {
                'opponent': ""
            }
        }
        form = CreateBattleForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('opponent', form.errors)

    def test_battle_form_valid(self):
        params = {
            'initial': {
                'creator': self.user.id
            },
            'data': {
                'opponent': mommy.make('users.User').id
            }
        }
        form = CreateBattleForm(**params)
        self.assertTrue(form.is_valid())


class TestChooseTeamForm(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')

    def test_pokemon_list_empty(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': "",
                'second_pokemon': "",
                'third_pokemon': ""
            }
        }

        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('first_pokemon', form.errors)
        self.assertIn('second_pokemon', form.errors)
        self.assertIn('third_pokemon', form.errors)

    def test_pokemon_creation_success(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }

        form = ChooseTeamForm(**params)
        self.assertTrue(form.is_valid(), form.errors)

    def test_choosing_first_pokemon_with_id_zero_returns_error(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': 0,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }

        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('first_pokemon', form.errors)

    def test_choosing_second_pokemon_with_id_zero_returns_error(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': 0,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }

        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('second_pokemon', form.errors)

    def test_choosing_third_pokemon_with_id_zero_returns_error(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': 0
            }
        }

        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('third_pokemon', form.errors)

    def test_pokemon_with_stats_equal_or_more_than_limit(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': self.battle
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=100, defense=100, hp=100).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=100, defense=100, hp=100).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }
        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())

    def test_picking_team_for_another_battle(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': mommy.make('battles.Battle')
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }
        form = ChooseTeamForm(**params)
        self.assertNotEqual(form.initial['battle_related'].id, self.battle.id)

    def test_picking_any_pokemon_that_already_exists_in_the_opponent_team(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': mommy.make('battles.Battle')
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }
        pokemons = mommy.make('pokemons.Pokemon',
                              _quantity=3, id=1)
        mommy.make('battles.BattleTeam',
                   trainer=mommy.make('users.User'),
                   pokemons=[pokemon for pokemon in pokemons],
                   battle_related=params['initial']['battle_related']
                   )
        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_picking_all_pokemon_that_already_exists_in_the_opponent_team(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': mommy.make('battles.Battle')
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id
            }
        }
        pokemons = mommy.make('pokemons.Pokemon',
                              _quantity=3, id=1)
        mommy.make('battles.BattleTeam',
                   trainer=mommy.make('users.User'),
                   pokemons=[pokemon for pokemon in pokemons],
                   battle_related=params['initial']['battle_related']
                   )
        form = ChooseTeamForm(**params)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_picking_distinct_pokemon_when_a_team_already_exists(self):
        params = {
            'initial': {
                'trainer': self.user,
                'battle_related': mommy.make('battles.Battle')
            },
            'data': {
                'first_pokemon': mommy.make(
                    'pokemons.Pokemon', id=1, attack=10, defense=10, hp=10).id,
                'second_pokemon': mommy.make(
                    'pokemons.Pokemon', id=2, attack=10, defense=10, hp=10).id,
                'third_pokemon': mommy.make(
                    'pokemons.Pokemon', id=3, attack=10, defense=10, hp=10).id
            }
        }
        pokemons = mommy.make('pokemons.Pokemon',
                              _quantity=3, id=5)
        mommy.make('battles.BattleTeam',
                   trainer=mommy.make('users.User'),
                   pokemons=[pokemon for pokemon in pokemons],
                   battle_related=params['initial']['battle_related']
                   )
        form = ChooseTeamForm(**params)
        self.assertTrue(form.is_valid())
