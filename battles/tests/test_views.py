from django.test import Client, TestCase
from django.urls import resolve, reverse_lazy

from model_mommy import mommy

from battles.models import Battle
from battles.views import CreateBattleView
from users.models import User


class TestCreateBattleView(TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:create-battle')
        self.battle = mommy.make('battles.Battle')
        self.user = User.objects.create_user(
            email = "test@vinta.com.br",
            password = "vintaisawesome"
        )
        self.user_opponent = User.objects.create_user(
            email = "opponent@vinta.com.br",
            password = "vintaisawesome"
        )
        self.battle_params = {
            "creator": self.user.id,
            "opponent": self.user_opponent.id
        }
        self.auth_client = Client()
        self.auth_client.login(email=self.user.email,
                               password=self.user.password)
    
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

    def test_redirection_if_not_logged(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_battle_was_created_in_db(self):
        response = self.client.post(self.view_url, self.battle_params)
        battle = Battle.objects.get(id=self.battle.id)
        self.assertTrue(response, battle)
