from django.test import TestCase

from model_mommy import mommy

from battles.helpers import (
    can_run_battle,
    compare_two_pokemons,
    check_run_battle_and_get_winner,
    send_email_when_battle_runs,
    generate_pokemon_label
)
from common.utils.tests import TestCaseUtils
from users.models import User
from battles.models import Battle


class TestBattle(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.creator_pokemon = mommy.make(
            'pokemons.Pokemon', name='Creatorpokemon', attack=60, defense=40, hp=30)
        self.opponent_pokemon = mommy.make(
            'pokemons.Pokemon', name='Opponentpokemon', attack=30, defense=50, hp=10)
        self.creator_battle_team = mommy.make(
            'battles.BattleTeam', pokemons=mommy.make('pokemons.Pokemon', _quantity=3),
            trainer=self.battle.creator
        )
        self.opponent_battle_team = mommy.make(
            'battles.BattleTeam', pokemons=mommy.make('pokemons.Pokemon', _quantity=3),
            trainer=self.battle.opponent
        )

    def add_related_battle_to_teams(self):
        self.creator_battle_team.battle_related = self.battle
        self.creator_battle_team.save()
        self.opponent_battle_team.battle_related = self.battle
        self.opponent_battle_team.save()

    def test_can_run_battle_with_a_team(self):
        self.add_related_battle_to_teams()
        self.assertTrue(can_run_battle(self.battle.id))

    def test_cannot_run_battle_without_a_team(self):
        self.assertFalse(can_run_battle(self.battle.id))

    def test_cannot_run_battle_with_just_one_team(self):
        self.creator_battle_team.battle_related = self.battle
        self.assertFalse(can_run_battle(self.battle.id))

    def test_two_pokemon_comparison(self):
        winner = compare_two_pokemons(
            self.creator_pokemon.id, self.opponent_pokemon.id)
        self.assertEqual(winner, self.creator_pokemon)

    def test_battle_running(self):
        self.add_related_battle_to_teams()
        self.assertNotEqual(
            check_run_battle_and_get_winner(self.battle.id), None)

    def test_if_battle_returns_a_winner(self):
        self.add_related_battle_to_teams()
        self.assertIsInstance(
            check_run_battle_and_get_winner(self.battle.id), User)

    def test_email_sending_to_participants(self):
        self.add_related_battle_to_teams()
        send_email_when_battle_runs(self.battle.id)

    def test_send_email_only_if_a_battle_can_run(self):
        self.assertFalse(can_run_battle(self.battle.id))
        self.assertEqual(send_email_when_battle_runs(self.battle.id), None)

    def test_generate(self):
        self.add_related_battle_to_teams()
        print(generate_pokemon_label(self.battle.id))