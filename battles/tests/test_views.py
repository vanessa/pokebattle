from django.test import TestCase
from django.urls import resolve, reverse_lazy

from model_mommy import mommy

from battles.forms import CreateBattleForm
from battles.models import Battle
from battles.views import BattleView, CreateBattleView
from common.utils.tests import TestCaseUtils


class TestCreateBattleView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:create-battle')
        self.user_opponent = mommy.make('users.User')
        self.battle = mommy.make('battles.Battle')
        self.view_class = CreateBattleView()
        self.battle_params = {
            'creator': self.user.id,
            'opponent': self.user_opponent.id
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
        response = self.auth_client.post(self.view_url, self.battle_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, response.url)

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertRedirects(
            response, expected_url='/login?next=/battles/create')

    def test_battle_was_created_in_db(self):
        response = self.client.post(self.view_url, self.battle_params)
        battle = Battle.objects.filter(id=self.battle.id).exists()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(battle)

    def test_create_battle_view_form(self):
        self.assertEqual(self.view_class.get_form_class(), CreateBattleForm)


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
        self.assertRedirects(
            response, expected_url='/login?next=/battles/details/{0}'.format(self.battle.id))
