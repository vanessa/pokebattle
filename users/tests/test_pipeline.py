from django.core import mail

import mock
from model_mommy import mommy
from social_django.utils import load_backend, load_strategy

from battles.models import Battle
from common.utils.tests import TestCaseUtils
from users.auth_pipeline import (
    create_invite_battle, send_inviter_email_when_battle_ready, validate_invite_key
)


class TestInviteSignup(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.strategy = load_strategy()
        self.backend = load_backend(strategy=self.strategy, name='google-oauth2', redirect_uri='/')

    @mock.patch('social_django.utils.load_strategy')
    def test_user_signed_up_with_invite(self, strategy):
        mommy.make('battles.Invite', key=123, invitee=self.user.email)
        strategy.session_get.return_value = '123'
        validate_invite_key(user=self.user, strategy=strategy,
                            backend=self.backend, details={})
        self.assertTrue(getattr(self.user, 'has_invite'))

    @mock.patch('social_django.utils.load_strategy')
    def test_user_signup_with_invite_creates_battle(self, strategy):
        mommy.make('battles.Invite', key=123, invitee=self.user.email)
        setattr(self.user, 'has_invite', True)
        strategy.session_get.return_value = '123'
        create_invite_battle(user=self.user, strategy=strategy,
                             backend=self.backend, details={})
        battles_count = Battle.objects.count()
        self.assertEqual(battles_count, 1)

    @mock.patch('social_django.utils.load_strategy')
    def test_invited_user_chooses_team_sends_email(self, strategy):
        # Set the user as an invited user who has
        # chosen a team and is ready to battle
        setattr(self.user, 'has_invite', True)
        setattr(self.user, 'invitee_ready', True)

        inviter_user = mommy.make('users.User')
        mommy.make('battles.Battle', opponent=self.user, creator=inviter_user)
        mommy.make('battles.Invite', key=123, invitee=self.user.email, inviter=inviter_user)
        strategy.session_get.return_value = '123'

        invitee_ready = getattr(self.user, 'invitee_ready', None)
        has_invite = getattr(self.user, 'has_invite', None)
        send_inviter_email_when_battle_ready(user=self.user, strategy=strategy,
                                             backend=self.backend, details={},
                                             pipeline_index=1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], inviter_user.email)
        self.assertTrue(invitee_ready)
        self.assertTrue(has_invite)
