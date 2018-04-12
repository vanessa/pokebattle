from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render  # noqa


class UserLoginView(LoginView):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)

class UserLogoutView(LogoutView):
    pass