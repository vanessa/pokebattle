from django.conf.urls import url

from .views import UserLoginView


urlpatterns = [
    url(r'^login$', UserLoginView.as_view(), name='login'),
]
