from django.urls import reverse

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
