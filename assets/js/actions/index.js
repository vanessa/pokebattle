import {
  AUTH_SET_TOKEN,
  AUTH_DISCARD_TOKEN,
  AUTH_SET_USER,
} from '../constants';

// TODO:

const authSetToken = token => ({
  type: AUTH_SET_TOKEN,
  token,
});

const authDiscardToken = () => ({
  type: AUTH_DISCARD_TOKEN,
});

const authSetUser = user => ({
  type: AUTH_SET_USER,
  user,
});

export {
  authSetToken,
  authDiscardToken,
  authSetUser,
};
