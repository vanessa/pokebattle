import { combineReducers } from 'redux';
import battle from './battleReducer';
import user from './userReducer';
import pokemon from './pokemonReducer';

const pokebattleReducer = combineReducers({
  battle,
  user,
  pokemon,
});

export default pokebattleReducer;
