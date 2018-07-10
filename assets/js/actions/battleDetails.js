import { normalize } from 'normalizr';
import { battle as battleDetailsSchema } from '../utils/schema';
import {
  BATTLE_SET_DETAILS,
  CLEAR_CURRENT_BATTLE,
} from '../constants/battle';
import Api from '../utils/api';

const battleSetDetails = payload => ({
  type: BATTLE_SET_DETAILS,
  payload,
});

const fetchAndSetBattleDetails = battleId => (
  dispatch => (
    Api.getBattleDetails(battleId)
    .then(battle => normalize(battle, battleDetailsSchema))
    .then(normalizedBattle => dispatch(battleSetDetails(normalizedBattle)))
    .catch(error => new Error(error))
  )
);

const clearCurrentBattle = payload => ({
  type: CLEAR_CURRENT_BATTLE,
  payload,
});

export {
  battleSetDetails,
  fetchAndSetBattleDetails,
  clearCurrentBattle,
};
