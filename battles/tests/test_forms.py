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
                'first_pokemon': mommy.make('pokemons.Pokemon', id=1).id,
                'second_pokemon': mommy.make('pokemons.Pokemon', id=2).id,
                'third_pokemon': mommy.make('pokemons.Pokemon', id=3).id
            }
        }

        form = ChooseTeamForm(**params)
        self.assertTrue(form.is_valid(), form.errors)
