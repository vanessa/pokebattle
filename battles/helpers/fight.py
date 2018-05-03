from pokemons.models import Pokemon


def compare_attack_to_defense(first_pokemon, second_pokemon):
    if first_pokemon.attack > second_pokemon.defense:
        return first_pokemon
    return second_pokemon


def compare_hp(creator_pokemon, opponent_pokemon):
    if creator_pokemon.hp > opponent_pokemon.hp:
        return creator_pokemon
    return opponent_pokemon


def get_pokemon_winner(creator_pokemon, opponent_pokemon):
    return compare_attack_to_defense(creator_pokemon, opponent_pokemon)


def check_tie_and_return_winner(creator_pokemon, opponent_pokemon):
    if compare_attack_to_defense(
        creator_pokemon, opponent_pokemon) != compare_attack_to_defense(
            opponent_pokemon, creator_pokemon):
        return compare_hp(creator_pokemon, opponent_pokemon)
    return get_pokemon_winner(creator_pokemon, opponent_pokemon)


def compare_two_pokemons(creator_pokemon_id, opponent_pokemon_id):
    creator_pokemon = Pokemon.objects.get(id=creator_pokemon_id)
    opponent_pokemon = Pokemon.objects.get(id=opponent_pokemon_id)

    return check_tie_and_return_winner(creator_pokemon, opponent_pokemon)
