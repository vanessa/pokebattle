from collections import Counter

from battles.helpers.emails import send_email_when_battle_finishes
from battles.helpers.fight import compare_two_pokemons
from battles.models import BattleTeam
from users.models import User


def can_run_battle(battle):
    if BattleTeam.objects.filter(battle_related=battle).count() == 2:
        return True
    return False


def mount_battle_list(battle):
    creator_team = BattleTeam.objects.get(
        battle_related=battle, trainer=battle.creator)
    opponent_team = BattleTeam.objects.get(
        battle_related=battle, trainer=battle.opponent)
    result = {}
    result['creator_team'] = [
        pokemon.id for pokemon in creator_team.pokemons.all()]
    result['opponent_team'] = [
        pokemon.id for pokemon in opponent_team.pokemons.all()]
    return result['creator_team'], result['opponent_team']


def get_winner_pokemon_list(battle):
    battle_list = mount_battle_list(battle)
    comparison_winners = []
    for creator_pokemon, opponent_pokemon in zip(battle_list[0], battle_list[1]):
        comparison_winners.append(compare_two_pokemons(
            creator_pokemon, opponent_pokemon))
    return comparison_winners


def get_the_battle_winner(battle):
    winner_list = get_winner_pokemon_list(battle)
    teams = BattleTeam.objects.filter(
        battle_related=battle, pokemons__in=winner_list)
    winner_trainer_id = Counter(
        [team.trainer.id for team in teams]).most_common()[0][0]
    battle_winner = User.objects.get(id=winner_trainer_id)
    return battle_winner


def run_battle(battle):
    if can_run_battle(battle):
        winner = get_the_battle_winner(battle)
        battle.winner = winner
        battle.save()
        send_email_when_battle_finishes(battle)
        return True
    return False


def teams_cannot_battle(first_team, second_team):
    if first_team:
        result = any(
            pokemon in first_team for pokemon in second_team)
        return result
    return False


def battle_team_existent(battle, second_team):
    existent_team_pokemon = BattleTeam.objects.filter(
        battle_related=battle
    ).first()
    if existent_team_pokemon:
        return teams_cannot_battle(existent_team_pokemon, second_team)
    return False
