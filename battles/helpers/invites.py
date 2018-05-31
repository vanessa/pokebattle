from django.utils.crypto import get_random_string

from battles.helpers.emails import send_inviter_email_when_invitee_chooses_team
from battles.models import Invite


def create_invite_key():
    key = get_random_string(12).lower()
    return key


def handle_invite_battle(user, battle):
    has_invite = getattr(user, 'has_invite', None)
    if not has_invite:
        return False
    setattr(user, 'has_invite', False)
    invite = Invite.objects.get(inviter=battle.creator, invitee=battle.opponent)
    invite.delete()
    return send_inviter_email_when_invitee_chooses_team(battle)
