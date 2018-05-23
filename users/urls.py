from django.conf.urls import url

from .views import UserInvitedProcessView, UserLoginView, UserLogoutView, UserSignupView


urlpatterns = [
    url(r'^login$', UserLoginView.as_view(), name='login'),
    url(r'^logout$', UserLogoutView.as_view(), name='logout'),
    url(r'^signup$', UserSignupView.as_view(), name='signup'),
    url(r'^invite/validate$', UserInvitedProcessView.as_view(), name='validate-invite')
]
