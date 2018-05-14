from django.core import mail
from django.test import TestCase
from django.urls import reverse

from model_mommy import mommy

from battles.helpers.emails import send_battle_invite_email


class TestBattleInviteEmail(TestCase):
    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')

    def test_email_is_sent_with_correct_url(self):
        send_battle_invite_email(self.battle)
        correct_url = reverse('battles:details', args={self.battle.id})
        self.assertTrue(correct_url in mail.outbox[0].body)
