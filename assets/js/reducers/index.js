import { combineReducers } from 'redux';
import battle from './battleReducer';
import user from './userReducer';

const pokebattleReducer = combineReducers({
  battle,
  user,
});

export default pokebattleReducer;
