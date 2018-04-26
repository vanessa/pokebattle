from collections import Counter

from battles.helpers.emails import send_email_when_battle_finishes
from battles.helpers.fight import compare_two_pokemons
from battles.models import BattleTeam
from users.models import User


# rw: use exists since you are doing nothing with the results.
# rw: is there a possibility for doesn't have it created?
# rw: maybe just check how many teams there is in one battle.
def can_run_battle(battle):
    try:
        BattleTeam.objects.get(
            battle_related=battle, trainer=battle.creator)
        BattleTeam.objects.get(
            battle_related=battle, trainer=battle.opponent)
    except BattleTeam.DoesNotExist:
        return False
    else:
        return True


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


# class Fight:
#
#     def __init__(self, first_pokemon, second_pokemon):
#         self.first_pokemon = first_pokemon
#         self.second_pokemon = second_pokemon
#
#     def compare_attack_to_defense(self):
#         if self.first_pokemon.attack > self.second_pokemon.defense:
#             return self.first_pokemon
#         return self.second_pokemon
#
#     def compare_hp(self):
#         if self.first_pokemon.hp > self.second_pokemon.hp:
#             return self.first_pokemon
#         return self.second_pokemon
#
#     def get_winner(self):
#         # do - it
#
#
# battle = Battle(team1, team2)
# battle.start()
# winner_team = batte.get_winner()
#
#
# class Battle:
#
#     def __init__(self, first_team, second_team):
#         self.first_team = first_team
#         self.second_team = second_team
#         self.fight = Fight
#         self.record = {'first_team': 0, 'second_team': 0}
#
#     def get_winner_team(self):
#         if self.record['first_team'] > self.record['second_team']:
#             return self.first_team
#         return self.second_team
#
#     def start(self):
#         first_team_pokemons = self.first_team.pokemons.all()
#         second_team_pokemons = self.second_team.pokemons.all()
#
#         for first_pokemon, second_pokemon in zip(first_team_pokemons, second_team_pokemons):
#             fight = self.fight(first_pokemon, second_pokemon)
#             pokemon_winner = fight.get_winner()
#             if pokemon_winner in first_team_pokemons:
#                 self.record['first_team'] += 1
#             else:
#                 self.record['second_team'] += 1


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

# rw: we are not used to use save when naming functions.
# rw: why are you puting those returns?
def check_run_battle_and_save_winner(battle):
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
