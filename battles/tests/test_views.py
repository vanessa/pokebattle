from django.test import Client, TestCase
from django.urls import resolve, reverse_lazy

from model_mommy import mommy

from battles.models import Battle, BattleTeam
from battles.views import (
    CreateBattleView,
    BattleView
)
from common.utils.tests import TestCaseUtils
from pokemons.models import Pokemon
from users.models import User


class TestCreateBattleView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:create-battle')
        self.battle = mommy.make('battles.Battle')
        self.user_opponent = mommy.make('users.User')
        self.battle_params = {
            "creator": self.user.id,
            "opponent": self.user_opponent.id
        }
    
    def test_response_status_200(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_create_battle_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            CreateBattleView.as_view().__name__
        )

    def test_battle_creation(self):
        response = self.client.post(self.view_url, self.battle_params)
        self.assertEqual(response.status_code, 302)

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_battle_was_created_in_db(self):
        response = self.client.post(self.view_url, self.battle_params)
        battle = Battle.objects.get(id=self.battle.id)
        self.assertTrue(response, battle)

class TestBattleDetailView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.pokemons = mommy.make('pokemons.Pokemon', _quantity=3)
        self.battle_team_creator = mommy.make('battles.BattleTeam',
                                              battle_related=self.battle,
                                              pokemons=self.pokemons,
                                              trainer=self.battle.creator)
        self.battle_team_opponent = mommy.make('battles.BattleTeam',
                                               battle_related=self.battle,
                                               pokemons=self.pokemons,
                                               trainer=self.battle.opponent)
        self.view_url = reverse_lazy('battles:details',
                                     kwargs={'pk': self.battle.id})

    def test_response_status_200(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_battle_details_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            BattleView.as_view().__name__
        )

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
