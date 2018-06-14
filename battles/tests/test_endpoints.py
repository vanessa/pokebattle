from django.urls import reverse

from model_mommy import mommy
from rest_framework import status

from common.utils.tests import TestCaseUtils


class TestBattleDetailsEndpoint(TestCaseUtils):
    def test_fetch_correct_battle(self):
        battle = mommy.make('battles.Battle', creator=self.user)
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        response = self.auth_client.get(view_url)
        data = response.json()

        self.assertEqual(data['creator']['username'], battle.creator.get_short_name())
        self.assertEqual(data['id'], battle.id)
        self.assertEqual(data['status'], battle.status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_fetch_other_battle_details(self):
        battle = mommy.make('battles.Battle')
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        response = self.client.get(view_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
