from .models import Battle, BattleTeam


def can_run_battle(battle_id):
    battle = Battle.objects.get(id=battle_id)
    try:
        BattleTeam.objects.get(
            battle_related=battle, trainer=battle.creator)
        BattleTeam.objects.get(
            battle_related=battle, trainer=battle.opponent)
    except BattleTeam.DoesNotExist:
        return False
    else:
        return True


def check_and_run_battle(battle_id):
    if can_run_battle(battle_id) is True:
        print('Go on')
    else:
        print('No!')
