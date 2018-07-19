import {
  BATTLE_SET_DETAILS,
  BATTLE_SET_LIST,
  BATTLE_CREATED_REDIRECT,
  BATTLE_CLEAR_REDIRECT,
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
    case BATTLE_CREATED_REDIRECT:
      return {
        ...state,
        battleRedirect: true,
      };
    case BATTLE_CLEAR_REDIRECT:
      return {
        ...state,
        battleRedirect: false,
      };
    default:
      return state;
  }
};

export default battle;

