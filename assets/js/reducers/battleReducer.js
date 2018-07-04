import {
  BATTLE_SET_DETAILS,
  BATTLE_SET_LIST,
} from '../constants/battle';

const battle = (state = [], action) => {
  switch (action.type) {
    case BATTLE_SET_DETAILS:
      return {
        ...state,
        [action.battle.id]: action.battle,
      };
    case BATTLE_SET_LIST:
      return {
        ...state,
        battleList: action.battleList,
      };
    default:
      return state;
  }
};

export default battle;

