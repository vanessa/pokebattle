import { normalize } from 'normalizr';
import {
  BATTLE_SET_LIST,
} from '../constants/battle';
import Api from '../utils/api';
import { battleList as battleListSchema } from '../utils/schema';

const battleSetList = payload => ({
  type: BATTLE_SET_LIST,
  payload,
});

const fetchAndSetBattleList = () => (
  dispatch => (
    Api.getBattleList()
    .then(battleList => normalize(battleList, battleListSchema))
    .then(normalizedBattleList => dispatch(battleSetList(normalizedBattleList)))
    .catch(error => new Error(error))
  )
);

export {
  battleSetList,
  fetchAndSetBattleList,
};
