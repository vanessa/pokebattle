import { BATTLE_CREATED_REDIRECT, BATTLE_CLEAR_REDIRECT } from '../constants/battle';
import Api from '../utils/api';

const battleCreatedRedirect = () => ({ type: BATTLE_CREATED_REDIRECT });

const battleClearRedirect = () => ({ type: BATTLE_CLEAR_REDIRECT });

const createBattleAndRedirect = battle => dispatch => (
  Api.createBattle(battle).then(
    () => dispatch(battleCreatedRedirect()),
    error => new Error(error),
  )
);

export default createBattleAndRedirect;
export {
  battleClearRedirect,
};
