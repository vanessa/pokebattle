import { LOAD_USERS } from '../constants/user';
import Api from '../utils/api';

const loadUsers = payload => ({
  type: LOAD_USERS,
  payload,
});

const fetchAndLoadUsers = () => dispatch => (
  Api.loadUsers().then(
    users => dispatch(loadUsers(users)),
    error => new Error(error),
  )
);

export default fetchAndLoadUsers;
