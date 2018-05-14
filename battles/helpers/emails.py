from django.conf import settings
from django.urls import reverse_lazy

from templated_email import send_templated_mail

from battles.models import BattleTeam


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
    battle_url = '{domain}{battle_details}'.format(
        domain=settings.DOMAIN,
        battle_details=reverse_lazy('battles:details', args={battle.pk})
    )
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
