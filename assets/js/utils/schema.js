import { schema } from 'normalizr';

const user = new schema.Entity('users');
const pokemon = new schema.Entity('pokemon');
const battle = new schema.Entity('battles', {
  opponent: {
    trainer: user,
    pokemons: [pokemon],
  },
  creator: {
    trainer: user,
    pokemons: [pokemon],
  },
  trainer: user,
  winner: user,
});

const battleList = [battle];

export {
  battle,
  battleList,
};
