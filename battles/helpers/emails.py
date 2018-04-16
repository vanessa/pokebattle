from django.conf import settings

from templated_email import send_templated_mail

from battles.models import Battle, BattleTeam
from users.models import User


def send_battle_result_email(user_id, battle_id):
    battle = Battle.objects.get(id=battle_id)
    user = User.objects.get(id=user_id)
    relative_opponent = battle.creator if battle.creator != user else battle.opponent
    kwargs = dict(
        template_name='battle_result',
        from_email=settings.DEFAULT_FROM_EMAIL,
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


def send_email_when_battle_finishes(battle_id):
    battle = Battle.objects.get(id=battle_id)
    for trainer in [battle.creator, battle.opponent]:
        return send_battle_result_email(trainer.id, battle.id)
