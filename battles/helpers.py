from pokemons.helpers import Pokemon

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

    def get_winner_if_not_tie():
        return compare_a1_to_d2()

    def compare_pokemon_hp():
        if creator_pokemon.hp > opponent_pokemon.hp:
            return creator_pokemon
        return opponent_pokemon

    if compare_a1_to_d2() != compare_a2_to_d1():
        winner = compare_pokemon_hp()
        return winner
    winner = get_winner_if_not_tie()
    return winner

def mount_battle_dict(battle_id):
    battle = Battle.objects.get(id=battle_id)
    creator_team = BattleTeam.objects.get(battle_related=battle, trainer=battle.creator)
    opponent_team = BattleTeam.objects.get(battle_related=battle, trainer=battle.opponent)
    result = []
    result[0] = [pokemon.id for pokemon in creator_team.pokemons.all()]
    result[1] = [pokemon.id for pokemon in opponent_team.pokemons.all()]
    return result

def check_and_run_battle(battle_id):
    if can_run_battle(battle_id) is True:
        pokemon = mount_battle_dict(battle_id)
        for creator_pokemon, opponent_pokemon in zip([iter(pokemon)]):
            print(creator_pokemon)
        # TODO run tests
    else:
        print('No!')
