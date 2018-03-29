from django.test import Client, TestCase

from model_mommy import mommy

from battles.forms import CreateBattleForm
from common.utils.tests import TestCaseUtils


class TestCreateBattleForm(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.opponent = mommy.make('users.User')
        self.battle_params = {
            'creator': self.user,
            'opponent': self.opponent
        }

    def test_init_with_null_entry(self):
        form = CreateBattleForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('opponent', form.errors)
    
    def test_no_opponent_selected(self):
        self.battle_params['opponent'] = ''
        form = CreateBattleForm(self.battle_params)
        self.assertFalse(form.is_valid())
        self.assertIn('opponent', form.errors)
