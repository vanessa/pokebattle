import {
  BATTLE_SET_LIST,
} from '../constants/battle';
import Api from '../utils/api';

const battleSetList = battleList => ({
  type: BATTLE_SET_LIST,
  battleList,
});

const fetchAndSetBattleList = () => (
  dispatch => (
    Api.getBattleList().then(
      list => dispatch(battleSetList(list)),
      error => new Error(error),
    )
  )
);

export {
  battleSetList,
  fetchAndSetBattleList,
};
