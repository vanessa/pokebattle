import { LOAD_POKEMON } from '../constants/pokemon';
import Api from '../utils/api';

const loadPokemonList = payload => ({
  type: LOAD_POKEMON,
  payload,
});

const fetchAndLoadPokemonList = () => dispatch => (
  Api.loadPokemonList().then(
    list => dispatch(loadPokemonList(list)),
    error => new Error(error),
  )
);

export default fetchAndLoadPokemonList;
