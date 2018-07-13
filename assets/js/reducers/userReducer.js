import { USER_SET_DETAILS, LOAD_USERS } from '../constants/user';

const user = (state = [], action) => {
  switch (action.type) {
    case USER_SET_DETAILS:
      return {
        ...state,
        details: action.details,
      };
    case LOAD_USERS:
      return {
        ...state,
        users: action.payload,
      };
    default:
      return state;
  }
};

export default user;
