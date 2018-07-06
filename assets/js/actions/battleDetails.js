import { normalize } from 'normalizr';
import { battle as battleSchema } from '../utils/schema';
import {
  BATTLE_SET_DETAILS,
} from '../constants/battle';
import Api from '../utils/api';

const battleSetDetails = payload => ({
  type: BATTLE_SET_DETAILS,
  payload,
});

const fetchAndSetBattleDetails = battleId => (
  dispatch => (
    Api.getBattleDetails(battleId)
    .then(battle => normalize(battle, battleSchema))
    .then(normalizedBattle => dispatch(battleSetDetails(normalizedBattle)))
    .catch(error => new Error(error))
  )
);

export {
  battleSetDetails,
  fetchAndSetBattleDetails,
};
