from django.urls import resolve, reverse_lazy

from common.utils.tests import TestCaseUtils
from users.forms import UserSignupForm
from users.views import UserSignupView


class TestUserSignupView(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('auth:signup')
        self.view_class = UserSignupView()
        self.success_url = reverse_lazy('battles:list')

    def test_user_signup_url_is_connected_to_view(self):
        self.assertEqual(resolve(self.view_url).func.__name__,
                         UserSignupView.as_view().__name__)

    def test_get_correct_form(self):
        form_class = self.view_class.get_form_class()
        self.assertEqual(form_class, UserSignupForm)

    def test_signup_view_redirects_authenticated_users(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_access_to_signup_view_returns_200(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_redirects_to_battle_list(self):
        user_params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.view_url, user_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_signup_redirection_has_welcome_message(self):
        user_params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.view_url, user_params)
        message_count = len(response.cookies['messages'])
        self.assertTrue(message_count > 0)

    def test_user_signup(self):
        user_params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.view_url, user_params)
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
