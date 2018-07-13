import {
  BATTLE_SET_LIST,
} from '../constants/battle';

const battle = (state = [], action) => {
  switch (action.type) {
    case BATTLE_SET_LIST:
      return {
        ...state,
        ...action.payload.entities,
        result: action.payload.result,
      };
    default:
      return state;
  }
};

export default battle;

