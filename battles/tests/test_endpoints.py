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
        self.assertEqual(data['creator']['trainer']['username'], battle.creator.username)
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
