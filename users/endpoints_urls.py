from django.conf.urls import url

from users.endpoints import UserDetailsEndpoint


urlpatterns = [
    url(r'^users/(?P<pk>[\w-]+)$', UserDetailsEndpoint.as_view(), name='user-details')
]
