from django.test import TestCase
from django.urls import reverse_lazy

from model_mommy import mommy  # noqa

from common.utils.tests import TestCaseUtils
from users.forms import UserSignupForm
from users.views import UserSignupView


class TestUserSignupView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('auth:signup')
        self.view_class = UserSignupView()

    def test_get_correct_form(self):
        form_class = self.view_class.get_form_class()
        self.assertEqual(form_class, UserSignupForm)

    def test_signup_view_redirects_authenticated_users(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 302)

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

    def test_signup_redirection_has_welcome_message(self):
        user_params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.view_url, user_params)
        message_count = len(response.cookies['messages'])
        self.assertTrue(message_count > 0)
