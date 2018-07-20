import json

from django.urls import reverse

from model_mommy import mommy
from rest_framework import status

from common.utils.tests import TestCaseUtils


class TestBattleDetailsEndpoint(TestCaseUtils):
    def test_fetch_correct_battle(self):
        battle = mommy.make('battles.Battle', creator=self.user)
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        response = self.auth_client.get(view_url)
        data = response.data
        self.assertEqual(data['creator']['trainer']['label'], battle.creator.username)
        self.assertEqual(data['id'], battle.id)
        self.assertEqual(data['status'], battle.status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_fetch_other_battle_details(self):
        battle = mommy.make('battles.Battle')
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        response = self.client.get(view_url)
        self.assertResponse403(response)


class TestBattleListEndpoint(TestCaseUtils):
    def test_fetch_correct_list(self):
        mommy.make('battles.Battle', creator=self.user, _quantity=3)
        view_url = reverse('api-battles:battle-list')
        response = self.auth_client.get(view_url)
        data = response.data
        self.assertEqual(len(data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_battles_that_user_participates(self):
        # Battles that user is creator or opponent
        mommy.make('battles.Battle', creator=self.user, _quantity=3)
        # Random battles which user isn't part of
        mommy.make('battles.Battle', _quantity=2)
        view_url = reverse('api-battles:battle-list')
        response = self.auth_client.get(view_url)
        data = response.data
        self.assertEqual(len(data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_fetch_battles_when_logged_out(self):
        view_url = reverse('api-battles:battle-list')
        response = self.client.get(view_url)
        self.assertResponse403(response)


class TestBattleCreationEndpoint(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = reverse('api-battles:create-battle')

    def test_battle_creation(self):
        # Create the instances
        mommy.make('users.User', id=2)
        mommy.make('pokemons.Pokemon', id=1)
        mommy.make('pokemons.Pokemon', id=2)
        mommy.make('pokemons.Pokemon', id=3)

        data = {
            "opponent": 2,
            "team": [
                {
                    "id": 3,
                    "name": "venusaur",
                    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png",  # noqa
                    "attack": 82,
                    "defense": 83,
                    "hp": 80
                },
                {
                    "id": 1,
                    "name": "bulbasaur",
                    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",  # noqa
                    "attack": 49,
                    "defense": 49,
                    "hp": 45
                },
                {
                    "id": 2,
                    "name": "charizard",
                    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",  # noqa
                    "attack": 84,
                    "defense": 78,
                    "hp": 78
                }
            ]
        }
        response = self.auth_client.post(self.view_url,
                                         json.dumps(data), content_type='application/json')
        self.assertResponse201(response)
