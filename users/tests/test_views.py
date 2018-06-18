from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import resolve, reverse

from model_mommy import mommy
from rest_framework.authtoken.models import Token

from common.utils.tests import TestCaseUtils
from users.forms import UserSignupForm
from users.views import UserInvitedProcessView, UserSignupView


class TestUserSignupView(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.view_url = reverse('auth:signup')
        self.view_class = UserSignupView()
        self.success_url = reverse('battles:list')

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


class TestUserSignupInvite(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.view_url = reverse('auth:validate-invite')

    def test_user_signup_redirection_with_invite(self):
        # Creating invite and battle
        invite = mommy.make('battles.Invite', invitee=self.user.email, key=123)
        battle = mommy.make('battles.Battle', creator=invite.inviter, opponent=self.user)

        request = self.factory.get(self.view_url)
        request.user = self.user

        # Adding invite_key to session
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session['invite_key'] = 123
        request.session.save()

        # Adding messages to request, since the view uses it
        # otherwise you'd get a django.contrib.messages.api.MessageFailure
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        battle_details_url = reverse('battles:details', kwargs={'pk': battle.pk})
        response = UserInvitedProcessView.as_view()(request)
        invite.refresh_from_db()  # Adding because of the invite.accepted = True on views
        self.assertResponse302(response)
        self.assertEqual(response.url, battle_details_url)
        self.assertTrue(invite.accepted)

    def test_user_signup_redirection_without_invite(self):
        response = self.auth_client.get(self.view_url)
        battles_list_url = reverse('battles:list')
        self.assertResponse302(response)
        self.assertEqual(response.url, battles_list_url)

    def test_user_token_is_created(self):
        # It's `auth` because of the user has already
        # been registered and this view is to validate
        # if they have a valid invite or not
        response = self.auth_client.post(self.view_url)
        token = Token.objects.filter(user=self.user)
        self.assertResponse302(response)
        self.assertEqual(token.count(), 1)
