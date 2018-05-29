from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail

from battles.models import BattleTeam


def _generate_battle_url(battle):
    battle_url = '{domain}{battle_details}'.format(
        domain=settings.DOMAIN,
        battle_details=reverse_lazy('battles:details', args={battle.pk})
    )
    return battle_url


def _send_battle_result_email(user, battle):
    relative_opponent = battle.creator if battle.creator != user else battle.opponent
    kwargs = dict(
        template_name='battle_result',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[user.email],
        context={
            'username': user.get_short_name(),
            'relative_opponent': relative_opponent.get_short_name(),
            'winner': battle.winner.get_short_name(),
            'your_team': BattleTeam.objects.get(battle_related=battle,
                                                trainer=user).pokemons.all(),
            'opponent_team': BattleTeam.objects.get(battle_related=battle,
                                                    trainer=relative_opponent
                                                    ).pokemons.all()
        }
    )
    return send_templated_mail(**kwargs)


def send_email_when_battle_finishes(battle):
    for trainer in [battle.creator, battle.opponent]:
        _send_battle_result_email(trainer, battle)


def send_battle_invite_email(battle):
    battle_url = _generate_battle_url(battle)
    kwargs = dict(
        template_name='battle_invite',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[battle.opponent.email],
        context={
            'username': battle.opponent.get_short_name(),
            'inviter': battle.creator.get_short_name(),
            'battle_url': battle_url
        }
    )
    return send_templated_mail(**kwargs)


def send_pokebattle_invite_email(invite):
    signup_url = '{domain}{signup}?key={invite_key}'.format(
        domain=settings.DOMAIN,
        signup=reverse_lazy('auth:login'),  # Signup and login are on the same page
        invite_key=invite.key
    )
    kwargs = dict(
        template_name='new_user_invite',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[invite.invitee],
        context={
            'signup_url': signup_url,
            'inviter': invite.inviter.get_short_name()
        }
    )
    return send_templated_mail(**kwargs)


def send_inviter_email_when_invitee_chooses_team(battle):
    kwargs = dict(
        template_name='user_accepted_invite',
        from_email=settings.SERVER_EMAIL,
        recipient_list=[battle.creator.email],
        context={
            'battle_url': _generate_battle_url(battle),
            'inviter': battle.creator,
            'invitee': battle.opponent
        }
    )
    return send_templated_mail(**kwargs)
