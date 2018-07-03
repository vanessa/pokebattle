import {
  USER_SET_DETAILS,
  USER_DELETE_DETAILS,
} from '../constants/user';
import Api from '../utils/api';

const userSetDetails = userDetails => ({
  type: USER_SET_DETAILS,
  details: userDetails,
});

const userDeleteDetails = userDetails => ({
  type: USER_DELETE_DETAILS,
  details: userDetails,
});

const fetchAndSetUserDetails = () => (
  dispatch => (
    Api.getUserInfo().then(
      user => dispatch(userSetDetails(user)),
      error => new Error(error),
    )
  )
);

export {
  userSetDetails,
  userDeleteDetails,
  fetchAndSetUserDetails,
};
