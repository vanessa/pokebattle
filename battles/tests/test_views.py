from django.test import Client, TestCase
from django.urls import resolve, reverse_lazy

from model_mommy import mommy

from battles.views import CreateBattleView


class TestCreateBattleView(TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:create-battle')
        self.battle = mommy.make('battles.Battle')
        self.user = mommy.make('users.User')
        self.user_opponent = mommy.make('users.User')
        self.battle_params = {
            "creator": self.user.id,
            "opponent": self.user_opponent.id
        }
    
    def test_response_status_200(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_create_battle_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            CreateBattleView.as_view().__name__
        )

    def test_battle_creation(self):
        response = self.client.post(self.view_url, self.battle_params)
        self.assertEqual(response.status_code, 302)