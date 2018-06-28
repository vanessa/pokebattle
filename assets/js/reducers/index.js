import { combineReducers } from 'redux';
import battle from './battle';

const pokebattleReducer = combineReducers({
  battle,
});

export default pokebattleReducer;
