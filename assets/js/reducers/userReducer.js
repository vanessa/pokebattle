import {
  USER_SET_DETAILS,
  USER_DELETE_DETAILS,
} from '../constants/user';

const user = (state = [], action) => {
  switch (action.type) {
    case USER_SET_DETAILS:
      return {
        ...state,
        details: action.details,
      };
    case USER_DELETE_DETAILS:
      return state.filter(({ id }) => id !== action.details.id);
    default:
      return state;
  }
};

export default user;
