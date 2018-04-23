from django.test import TestCase
from django.urls import reverse_lazy

from model_mommy import mommy  # noqa

from common.utils.tests import TestCaseUtils
from users.views import UserSignupView  # noqa


class TestUserSignupView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('auth:signup')

    def test_signup_redirects_to_battle_list(self):
        user_params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.view_url, user_params)
        success_url = reverse_lazy('battles:list')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, success_url)
