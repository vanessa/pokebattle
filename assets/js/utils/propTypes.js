import PropTypes from 'prop-types';

export const pokemonShape = {
  id: PropTypes.number,
  name: PropTypes.string,
  sprite: PropTypes.string,
  attack: PropTypes.number,
  defense: PropTypes.number,
  hp: PropTypes.number,
};

export const userShape = {
  id: PropTypes.number,
  username: PropTypes.string,
};
