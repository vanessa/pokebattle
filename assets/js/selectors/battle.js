import { denormalize } from 'normalizr';
import { battle as battleSchema } from '../utils/schema';

export const selectHydratedBattle = (id, state) => denormalize(id, battleSchema, state); // eslint-disable-line import/prefer-default-export,max-len
