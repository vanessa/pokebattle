from django.http import HttpResponseRedirect
from django.urls import reverse

from social_core.pipeline.partial import partial

from battles.helpers.emails import send_inviter_email_when_invitee_chooses_team
from battles.models import Battle, Invite


def validate_invite_key(strategy, details, backend, user=None, *args, **kwargs):  # noqa
    invite_key = strategy.session_get('invite_key')
    invite = Invite.objects.filter(key=invite_key, invitee=user.email)

    if not invite.exists():
        return
    setattr(user, 'has_invite', True)
    return


def create_invite_battle(strategy, details, backend, user=None, *args, **kwargs):  # noqa
    invite_key = strategy.session_get('invite_key')
    user_has_invite = getattr(user, 'has_invite', None)
    if not user_has_invite:
        return
    invite = Invite.objects.get(key=invite_key, invitee=user.email)
    Battle.objects.create(creator=invite.inviter, opponent=user)
    return


@partial
def send_inviter_email_when_battle_ready(strategy, details, backend, user=None, *args, **kwargs):  # noqa
    invitee_ready = getattr(user, 'invitee_ready', None)
    invite_key = strategy.session_get('invite_key')
    invite = Invite.objects.get(key=invite_key, invitee=user.email)
    battle = Battle.objects.get(creator=invite.inviter, opponent=user)

    if not invitee_ready:
        return HttpResponseRedirect(reverse('battles:details', args={battle.pk}))
    send_inviter_email_when_invitee_chooses_team(battle)
    return
