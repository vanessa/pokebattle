import {
  BATTLE_SET_DETAILS,
  BATTLE_SET_LIST,
  CLEAR_CURRENT_BATTLE,
} from '../constants/battle';

const battle = (state = [], action) => {
  switch (action.type) {
    case BATTLE_SET_DETAILS:
      return {
        ...state,
        currentBattle: { ...action.payload.entities.battles[action.payload.result] },
      };
    case BATTLE_SET_LIST:
      return {
        ...state,
        ...action.payload.entities,
        result: action.payload.result,
      };
    case CLEAR_CURRENT_BATTLE:
      return {
        ...state,
        currentBattle: {},
      };
    default:
      return state;
  }
};

export default battle;

