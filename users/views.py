from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from battles.models import Battle, Invite

from .forms import UserSignupForm


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invite_key'] = self.request.GET.get('key')
        return context


class UserLogoutView(LogoutView):
    pass


class UserSignupView(generic.CreateView):
    form_class = UserSignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('battles:list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

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


class UserInvitedProcessView(generic.RedirectView):
    url = reverse_lazy('battles:list')

    def get_redirect_url(self, *args, **kwargs):
        invite_key = self.request.session.get('invite_key')
        user = self.request.user
        invite = Invite.objects.get(invitee=user.email, key=invite_key)
        battle = Battle.objects.get(creator=invite.inviter, opponent=user)
        if not invite_key:
            return super().get_redirect_url(*args, **kwargs)
        messages.success(
            self.request,
            'Thanks for joining, {0}! How about you pick the Pokemon for your very first'
            ' battle against {1}?'.format(user.get_short_name(), battle.creator.get_short_name())
        )
        return reverse('battles:details', args=[battle.pk])
