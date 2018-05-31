from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string


def create_invite_key():
    key = get_random_string(12).lower()
    return key


def handle_invite_battle(user):
    has_invite = getattr(user, 'has_invite', None)
    if not has_invite:
        return False
    setattr(user, 'invitee_ready', True)
    return HttpResponseRedirect(reverse('social:complete', args=('google-oauth2',)))
