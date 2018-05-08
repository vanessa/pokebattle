from django.test import Client, TestCase

from users.forms import UserSignupForm


class TestUserSignupForm(TestCase):

    def setUp(self):
        self.client = Client()

    def test_init_with_null_entry(self):
        form = UserSignupForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_sending_with_not_equal_passwords(self):
        params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword1',
            'password2': 'tEsTpAsSWoRd49'
        }
        form = UserSignupForm(params)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_signup_form_works_correctly(self):
        params = {
            'email': 'test@vinta.com.br',
            'password1': 'testpassword1',
            'password2': 'testpassword1'
        }
        form = UserSignupForm(params)
        user = form.save()
        self.assertTrue(form.is_valid())
        self.assertEqual(user.email, params['email'])
