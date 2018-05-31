from battles.models import Battle, Invite


def validate_invite_key(strategy, details, backend, user=None, *args, **kwargs):  # noqa
    invite_key = strategy.session_get('invite_key')
    invite = Invite.objects.filter(key=invite_key, invitee=user.email)

    if not invite.exists():
        return
    setattr(user, 'has_invite', True)
    user.save()
    return


def create_invite_battle(strategy, details, backend, user=None, *args, **kwargs):  # noqa
    invite_key = strategy.session_get('invite_key')
    user_has_invite = getattr(user, 'has_invite', None)
    if not user_has_invite:
        return
    invite = Invite.objects.get(key=invite_key, invitee=user.email)
    Battle.objects.create(creator=invite.inviter, opponent=user)
    return
