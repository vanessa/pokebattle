import { denormalize } from 'normalizr';
import { battle as battleSchema } from '../utils/schema';

export const selectHydratedBattle = (id, state) => denormalize(id, battleSchema, state);
export const selectHydratedBattleList = state => denormalize(
  state.result, [battleSchema], state);
