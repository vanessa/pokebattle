
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserSignupForm


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass


class UserSignupView(generic.CreateView):
    form_class = UserSignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('battles:list')

    def form_valid(self, form):
        user = form.save()
        new_user = authenticate(
            username=user.email,
            password=self.request.POST['password1']
        )
        login(self.request, new_user)
        messages.info(
            self.request,
            'Thanks for signing up!'
        )
        return HttpResponseRedirect(self.success_url)
