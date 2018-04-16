from collections import Counter

from battles.helpers.fight import compare_two_pokemons
from battles.models import Battle, BattleTeam
from users.models import User


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


def mount_battle_list(battle_id):
    battle = Battle.objects.get(id=battle_id)
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


def get_winner_pokemon_list(battle_id):
    battle_list = mount_battle_list(battle_id)
    comparison_winners = []
    for creator_pokemon, opponent_pokemon in zip(battle_list[0], battle_list[1]):
        comparison_winners.append(compare_two_pokemons(
            creator_pokemon, opponent_pokemon))
    return comparison_winners


def get_the_battle_winner(battle_id):
    winner_list = get_winner_pokemon_list(battle_id)
    teams = BattleTeam.objects.filter(
        battle_related__id=battle_id, pokemons__in=winner_list)
    winner_trainer_id = Counter(
        [team.trainer.id for team in teams]).most_common()[0][0]
    battle_winner = User.objects.get(id=winner_trainer_id)
    return battle_winner


def check_run_battle_and_return_winner(battle_id):
    if can_run_battle(battle_id):
        return get_the_battle_winner(battle_id)
    return False
