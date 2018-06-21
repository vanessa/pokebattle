from django.conf.urls import url

from users.endpoints import UserDetailsEndpoint


urlpatterns = [
    url(r'^user-details$', UserDetailsEndpoint.as_view(), name='user-details')
]
