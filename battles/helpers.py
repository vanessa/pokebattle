from pokemons.helpers import Pokemon

from .models import Battle, BattleTeam
from users.models import User
from collections import Counter


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


def compare_two_pokemons(creator_pokemon_id, opponent_pokemon_id):
    creator_pokemon = Pokemon.objects.get(id=creator_pokemon_id)
    opponent_pokemon = Pokemon.objects.get(id=opponent_pokemon_id)

    def compare_a1_to_d2():
        if creator_pokemon.attack > opponent_pokemon.defense:
            return creator_pokemon
        return opponent_pokemon

    def compare_a2_to_d1():
        if opponent_pokemon.attack > creator_pokemon.defense:
            return opponent_pokemon
        return creator_pokemon

    def get_pokemon_winner():
        return compare_a1_to_d2()

    def compare_pokemon_hp():
        if creator_pokemon.hp > opponent_pokemon.hp:
            return creator_pokemon
        return opponent_pokemon

    if compare_a1_to_d2() != compare_a2_to_d1():
        winner = compare_pokemon_hp()
        return winner

    winner = get_pokemon_winner()
    return winner


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


def run_battle_and_get_winner(battle_id):

    def get_pokemon_winner_list():
        battle_list = mount_battle_list(battle_id)
        comparison_winners = []
        for creator_pokemon, opponent_pokemon in zip(battle_list[0], battle_list[1]):
            comparison_winners.append(compare_two_pokemons(
                creator_pokemon, opponent_pokemon))
        return comparison_winners

    def get_winner():
        winner_list = get_pokemon_winner_list()
        teams = BattleTeam.objects.filter(
            battle_related__id=battle_id, pokemons__in=winner_list)
        winner_trainer_id = Counter(
            [team.trainer.id for team in teams]).most_common()[0][0]
        battle_winner = User.objects.get(id=winner_trainer_id)
        return battle_winner

    def check_and_run_battle():
        battle = Battle.objects.get(id=battle_id)
        if can_run_battle(battle_id) is True:
            return get_winner()
        else:
            print('Battle cannot be ran')

    return check_and_run_battle()
