import mock
from model_mommy import mommy
from social_django.utils import load_backend, load_strategy

from battles.models import Battle
from common.utils.tests import TestCaseUtils
from users.auth_pipeline import _handle_invite


class TestInviteSignup(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.strategy = load_strategy()
        self.backend = load_backend(strategy=self.strategy, name='google-oauth2', redirect_uri='/')

    @mock.patch('users.auth_pipeline.validate_invite_key')
    def test_user_signed_up_with_invite(self, validate_key):
        mommy.make('battles.Invite', key=123)
        validate_key.return_value = setattr(self.user, 'has_invite', True)
        validate_key(user=self.user, strategy=self.strategy,
                     backend=self.backend, details={})
        self.assertTrue(getattr(self.user, 'has_invite'))

    def test_user_signup_with_invite_creates_battle(self):
        invite = mommy.make('battles.Invite', key=123, invitee=self.user.email)
        _handle_invite(invite, self.user)
        battles_count = Battle.objects.count()
        self.assertEqual(battles_count, 1)
        self.assertTrue(invite.accepted)
