export default class BattleHelpers {
  static userHasChosenTeam(battle, user) {
    const creatorOrOpponent = battle.creator.trainer.username === user.username ? 'creator' : 'opponent';
    return Array.isArray(battle[creatorOrOpponent].pokemons);
  }

  static getUserTeam(battle, user) {
    const creatorOrOpponent = battle.creator.trainer.username === user.username ? 'creator' : 'opponent';
    return battle[creatorOrOpponent].pokemons;
  }
}
