import { LOAD_POKEMON } from '../constants/pokemon';

const pokemon = (state = [], action) => {
  switch (action.type) {
    case LOAD_POKEMON:
      return {
        ...state,
        list: [...action.payload],
      };
    default:
      return state;
  }
};

export default pokemon;
