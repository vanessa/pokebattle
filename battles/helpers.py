from collections import Counter

from django.conf import settings

from templated_email import send_templated_mail

from pokemons.helpers import Pokemon
from users.models import User

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


def get_pokemon_winner_list(battle_id):
    battle_list = mount_battle_list(battle_id)
    comparison_winners = []
    for creator_pokemon, opponent_pokemon in zip(battle_list[0], battle_list[1]):
        comparison_winners.append(compare_two_pokemons(
            creator_pokemon, opponent_pokemon))
    return comparison_winners


def check_run_battle_and_get_winner(battle_id):

    def get_winner():
        winner_list = get_pokemon_winner_list(battle_id)
        teams = BattleTeam.objects.filter(
            battle_related__id=battle_id, pokemons__in=winner_list)
        winner_trainer_id = Counter(
            [team.trainer.id for team in teams]).most_common()[0][0]
        battle_winner = User.objects.get(id=winner_trainer_id)
        return battle_winner

    def check_and_run_battle():
        if can_run_battle(battle_id) is True:
            return get_winner()
        return False

    return check_and_run_battle()


def send_email_when_battle_runs(battle_id):
    battle = Battle.objects.get(id=battle_id)

    def send_email_to_trainer(user_id):
        user = User.objects.get(id=user_id)
        relative_opponent = battle.creator if battle.creator != user else battle.opponent
        send_templated_mail(
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
                                                        trainer=relative_opponent).pokemons.all()
            }
        )
    return [send_email_to_trainer(user.id) for user in [battle.creator, battle.opponent]]
