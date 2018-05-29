from collections import Counter

from battles.helpers.emails import send_email_when_battle_finishes
from battles.helpers.fight import compare_two_pokemons
from battles.models import BattleTeam
from users.models import User


def can_run_battle(battle):
    creator_team = BattleTeam.objects.filter(battle_related=battle, trainer=battle.creator).exists()
    opponent_team = BattleTeam.objects.filter(
        battle_related=battle, trainer=battle.opponent).exists()
    return creator_team and opponent_team


def mount_battle_list(battle):
    creator_team = BattleTeam.objects.get(battle_related=battle, trainer=battle.creator)
    opponent_team = BattleTeam.objects.get(battle_related=battle, trainer=battle.opponent)
    result = {
        'creator_team': [pokemon.id for pokemon in creator_team.pokemons.all()],
        'opponent_team': [pokemon.id for pokemon in opponent_team.pokemons.all()]
    }
    return result['creator_team'], result['opponent_team']


def get_winner_pokemon_list(battle):
    battle_list = mount_battle_list(battle)
    comparison_winners = []
    for creator_pokemon, opponent_pokemon in zip(battle_list[0], battle_list[1]):
        comparison_winners.append(compare_two_pokemons(
            creator_pokemon, opponent_pokemon))
    return comparison_winners


def get_battle_winner(battle):
    winner_list = get_winner_pokemon_list(battle)
    teams = BattleTeam.objects.filter(
        battle_related=battle, pokemons__in=winner_list)
    winner_trainer_id = Counter([team.trainer.id for team in teams]).most_common()[0][0]
    battle_winner = User.objects.get(id=winner_trainer_id)
    return battle_winner


def process_battle(battle):
    if not can_run_battle(battle):
        return False
    battle.status = 'P'
    battle.save()
    return True


def run_battle(battle):
    if not can_run_battle(battle):
        return False
    winner = get_battle_winner(battle)
    battle.winner = winner
    battle.status = 'F'
    battle.save()
    send_email_when_battle_finishes(battle)
    return True


def can_teams_battle(first_team, second_team):
    if not first_team:
        return False
    result = any(pokemon in first_team for pokemon in second_team)
    return result


def battle_team_existent(battle, second_team):
    existent_team_pokemon = BattleTeam.objects.filter(battle_related=battle).first()
    if existent_team_pokemon:
        return can_teams_battle(existent_team_pokemon, second_team)
    return False
