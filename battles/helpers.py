from .models import BattleTeam


def can_run_battle(battle):
    creator_team = BattleTeam.objects.filter(
        battle_related=battle, trainer=battle.creator).exists()
    opponent_team = BattleTeam.objects.filter(
        battle_related=battle, trainer=battle.opponent).exists()
    return creator_team and opponent_team


def check_and_run_battle(battle):
    if can_run_battle(battle):
        print('Go on')
    else:
        print('No!')


def has_team_duplicate_pokemon(pokemon_list):
    return len(set(pokemon_list)) != 3


def has_request_user_chosen_a_team(battle_pk, user):
    battle_team = BattleTeam.objects.filter(
        battle_related__pk=battle_pk,
        trainer=user
    )
    return battle_team.exists()
