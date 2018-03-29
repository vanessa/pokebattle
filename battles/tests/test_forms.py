from django.test import Client, TestCase

from model_mommy import mommy

from battles.forms import CreateBattleForm

class TestCreateBattleForm(TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        