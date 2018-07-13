from django.urls import reverse

from model_mommy import mommy

from common.utils.tests import TestCaseUtils


class TestUserDetailsEndpoint(TestCaseUtils):
    def test_authenticated_user_access_their_own_info(self):
        view_url = reverse('api-users:user-details')
        response = self.auth_client.get(view_url)
        self.assertResponse200(response)

    def test_not_authenticated_user_gets_error(self):
        view_url = reverse('api-users:user-details')
        response = self.client.get(view_url)
        self.assertResponse403(response)


class TestUserListEndpoint(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = reverse('api-users:users')

    def test_correct_list_length(self):
        users = mommy.make('users.User', _quantity=3, _fill_optional=['username'])
        response = self.auth_client.get(self.view_url)
        self.assertEqual(len(users), len(response.data))
        self.assertResponse200(response)

    def test_correct_response(self):
        users = mommy.make('users.User', _quantity=3, _fill_optional=['username'])
        response = self.auth_client.get(self.view_url)

        # Random pick someone
        picked_mommy_user = users[2]
        picked_response_user = response.data[2]

        self.assertEqual(picked_mommy_user.username, picked_response_user['label'])
        self.assertEqual(picked_mommy_user.id, picked_response_user['value'])
        self.assertResponse200(response)

    def test_not_authenticated_user_is_forbidden(self):
        response = self.client.get(self.view_url)
        self.assertResponse403(response)

    def test_user_excluded_from_list(self):
        mommy.make('users.User', _quantity=3, _fill_optional=['username'])
        response = self.auth_client.get(self.view_url)
        self.assertTrue(self.user not in response.data)
        self.assertResponse200(response)
