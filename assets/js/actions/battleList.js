import {
  BATTLE_SET_LIST,
} from '../constants';

const battleSetList = battleList => ({
  type: BATTLE_SET_LIST,
  battleList,
});

export default battleSetList;
