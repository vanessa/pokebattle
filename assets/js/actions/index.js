import {
  BATTLE_SET_DETAILS,
} from '../constants';

const battleSetDetails = battle => ({
  type: BATTLE_SET_DETAILS,
  battle,
});

export default {
  battleSetDetails,
};
