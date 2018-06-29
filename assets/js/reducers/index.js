import { combineReducers } from 'redux';
import battle from './battleReducer';

const pokebattleReducer = combineReducers({
  battle,
});

export default pokebattleReducer;
