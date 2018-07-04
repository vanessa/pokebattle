import USER_SET_DETAILS from '../constants/user';

const user = (state = [], action) => {
  switch (action.type) {
    case USER_SET_DETAILS:
      return {
        ...state,
        details: action.details,
      };
    default:
      return state;
  }
};

export default user;
