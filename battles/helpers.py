from .models import Battle, BattleTeam


def can_run_battle(battle):
    creator_team = BattleTeam.objects.filter(battle_related=battle, trainer=battle.creator).exists()
    opponent_team = BattleTeam.objects.filter(battle_related=battle, trainer=battle.opponent).exists()
    return creator_team and opponent_team


def check_and_run_battle(battle_id):
    if can_run_battle(battle_id) is True:
        print('Go on')
    else:
        print('No!')