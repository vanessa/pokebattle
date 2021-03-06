from django.core import mail

from model_mommy import mommy

from battles.helpers.battle import can_run_battle, can_teams_battle, run_battle
from battles.helpers.emails import send_email_when_battle_finishes
from battles.helpers.fight import compare_attack_to_defense, compare_hp
from battles.helpers.invites import handle_invite_battle
from battles.models import Invite
from common.utils.tests import TestCaseUtils
from users.models import User


class TestBattleHelper(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.creator_pokemon = mommy.make('pokemons.Pokemon', name='Creatorpokemon', attack=60,
                                          defense=20, hp=30)
        self.opponent_pokemon = mommy.make('pokemons.Pokemon', name='Opponentpokemon', attack=30,
                                           defense=50, hp=10)
        self.creator_battle_team = mommy.make('battles.BattleTeam', pokemons=mommy.make(
            'pokemons.Pokemon', _quantity=3, name='CreatorPokemon'), trainer=self.battle.creator)
        self.opponent_battle_team = mommy.make('battles.BattleTeam', pokemons=mommy.make(
            'pokemons.Pokemon', _quantity=3, name='OpponentPokemon'), trainer=self.battle.opponent)

    def _add_related_battle_for_teams(self):
        self.creator_battle_team.battle_related = self.battle
        self.creator_battle_team.save()
        self.opponent_battle_team.battle_related = self.battle
        self.opponent_battle_team.save()

    def test_can_run_battle_with_two_teams(self):
        self._add_related_battle_for_teams()
        self.assertTrue(can_run_battle(self.battle))

    def test_cannot_run_battle_without_a_team(self):
        self.assertFalse(can_run_battle(self.battle))

    def test_cannot_run_battle_with_just_one_of_two_teams(self):
        self.creator_battle_team.battle_related = self.battle
        self.creator_battle_team.save()
        self.assertFalse(can_run_battle(self.battle))

    def test_pokemon_attack_to_defense_comparison(self):
        winner = compare_attack_to_defense(self.creator_pokemon, self.opponent_pokemon)
        self.assertEqual(winner, self.creator_pokemon)

    def test_pokemon_hp_comparison(self):
        winner = compare_hp(self.creator_pokemon, self.opponent_pokemon)
        self.assertEqual(winner, self.creator_pokemon)

    def test_if_battle_returns_a_winner(self):
        self._add_related_battle_for_teams()
        run_battle(self.battle)
        self.assertIsInstance(self.battle.winner, User)

    def test_email_sending_to_participants(self):
        self._add_related_battle_for_teams()
        self.battle.winner = self.battle.opponent
        self.battle.save()
        send_email_when_battle_finishes(self.battle)
        self.assertIsInstance(self.battle.winner, User)

    def test_error_for_not_distinct_teams(self):
        example_existent_pokemon = mommy.make('pokemons.Pokemon', _quantity=3, id=2)
        random_pokemon = mommy.make('pokemons.Pokemon', _quantity=3, id=2)
        result = can_teams_battle(example_existent_pokemon, random_pokemon)
        self.assertTrue(result)

    def test_success_for_distinct_teams(self):
        example_existent_pokemon = mommy.make('pokemons.Pokemon', _quantity=3, id=2)
        random_pokemon = mommy.make('pokemons.Pokemon', _quantity=3)
        result = can_teams_battle(example_existent_pokemon, random_pokemon)
        self.assertFalse(result)

    def test_just_one_team_doesnt_run_task(self):
        self.creator_battle_team.battle_related = self.battle
        self.creator_battle_team.save()
        self.assertFalse(run_battle(self.battle))


class TestInviteHelper(TestCaseUtils):

    def test_user_without_invite(self):
        battle = mommy.make('battles.Battle', opponent=self.user)
        helper = handle_invite_battle(battle)
        self.assertFalse(helper)

    def test_user_with_invite_calls_handler(self):
        inviter_user = mommy.make('users.User')
        battle = mommy.make('battles.Battle', opponent=self.user, creator=inviter_user)
        mommy.make('battles.Invite', invitee=self.user.email, inviter=inviter_user)

        handle_invite_battle(battle)

        # Check if invite was deleted
        invite_queryset = Invite.objects.filter(
            invitee=self.user.email, inviter=inviter_user).count()

        self.assertEqual(len(mail.outbox), 1)  # assert email is sent
        self.assertEqual(invite_queryset, 0)

    def test_user_without_invite_doesnt_call_handler(self):
        inviter_user = mommy.make('users.User')
        battle = mommy.make('battles.Battle', opponent=self.user, creator=inviter_user)
        mommy.make('battles.Invite', invitee=self.user.email, inviter=inviter_user)

        handler = handle_invite_battle(battle)
        self.assertFalse(handler)
