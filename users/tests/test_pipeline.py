import mock
from model_mommy import mommy
from social_django.utils import load_backend, load_strategy

from battles.models import Battle
from common.utils.tests import TestCaseUtils
from users.auth_pipeline import create_invite_battle, validate_invite_key


class TestInvitePipeline(TestCaseUtils):

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
