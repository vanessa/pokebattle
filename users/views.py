from django.shortcuts import render  # noqa
from django.views import generic


class LoginView(generic.TemplateView):
    template_name = 'auth/login.html'
