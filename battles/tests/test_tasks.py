import mock
from model_mommy import mommy

from common.utils.tests import TestCaseUtils


class TestBattleTasks(TestCaseUtils):

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

    @mock.patch('battles.tasks.battle.run_battle_task')
    def test_calling_run_battle_task_calls_run_battle(self, run_battle_mock):
        self._add_related_battle_for_teams()
        run_battle_mock(self.battle.id)
        # TODO: run_battle is not being called!
