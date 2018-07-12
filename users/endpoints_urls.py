from django.conf.urls import url

from users.endpoints import UserDetailsEndpoint, UsersEndpoint


urlpatterns = [
    url(r'^user-details/$', UserDetailsEndpoint.as_view(), name='user-details'),
    url(r'^users/$', UsersEndpoint.as_view(), name='users'),
]
