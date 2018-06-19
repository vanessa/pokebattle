from django.urls import reverse

from model_mommy import mommy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from battles.endpoints import BattleDetailsEndpoint
from common.utils.tests import TestCaseUtils


class TestBattleDetailsEndpoint(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        # I couldn't mock this one because it gives me this error:
        # `ValueError: too many values to unpack (expected 2)`
        # When this runs: app_label, model_name = name.split('.')
        self.token = Token.objects.create(user=self.user)

    def test_fetch_correct_battle(self):
        battle = mommy.make('battles.Battle', creator=self.user)
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        request = self.factory.get(view_url)
        force_authenticate(request, user=self.user)
        response = BattleDetailsEndpoint.as_view()(request, pk=battle.pk)
        self.assertEqual(response.data['creator']['username'], battle.creator.get_short_name())
        self.assertEqual(response.data['id'], battle.id)
        self.assertEqual(response.data['status'], battle.status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_fetch_other_battle_details(self):
        battle = mommy.make('battles.Battle')
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        request = self.factory.get(view_url)
        force_authenticate(request, user=self.user)
        response = BattleDetailsEndpoint.as_view()(request, pk=battle.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_for_not_logged_Users(self):
        battle = mommy.make('battles.Battle')
        view_url = reverse('api-battles:battle-details', args=[battle.pk])
        request = self.factory.get(view_url)
        response = BattleDetailsEndpoint.as_view()(request, pk=battle.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
