import {
  BATTLE_SET_DETAILS,
} from '../constants';
import Api from '../utils/api';

const battleSetDetails = battle => ({
  type: BATTLE_SET_DETAILS,
  battle,
});

const fetchAndSetBattleDetails = battleId => (
  dispatch => (
    Api.getBattleDetails(battleId).then(
      battle => dispatch(battleSetDetails(battle)),
      error => new Error(error),
    )
  )
);

export {
  battleSetDetails,
  fetchAndSetBattleDetails,
};
