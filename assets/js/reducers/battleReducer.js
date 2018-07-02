import {
  BATTLE_SET_DETAILS,
} from '../constants';

const battle = (state = [], action) => {
  switch (action.type) {
    case BATTLE_SET_DETAILS:
      return {
        ...state,
        [action.battle.id]: action.battle,
      };
    default:
      return state;
  }
};

export default battle;
