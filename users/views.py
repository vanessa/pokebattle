from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render  # noqa


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass
