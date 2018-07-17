import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import VirtualizedSelect from 'react-virtualized-select';
import 'react-select/dist/react-select.css';
import 'react-virtualized-select/styles.css';
import fetchAndLoadPokemonList from '../actions/pokemon';
import fetchAndLoadUsers from '../actions/users';
import { pokemonShape } from '../utils/propTypes';

const SelectedPokemonCard = (props) => {
  const { pokemon, setFieldValue, name } = props;

  const clearSelection = () => {
    setFieldValue(name, null);
  };

  return (
    <div className="pokemon-chosen-card">
      <img src={pokemon.sprite} alt={pokemon.label} />
      <div className="pokemon-name">{pokemon.label}</div>
      <div className="pokemon-stats">
        A: {pokemon.attack} | D: {pokemon.defense} | HP: {pokemon.hp}
      </div>
      <div
        className="clear-button"
        role="presentation"
        onClick={clearSelection}
      >
        Clear
      </div>
    </div>
  );
};

const PokemonOption = (props) => {
  const {
    option,
    selectValue,
    focusedOption,
    focusOption,
  } = props;

  return (
    <div
      className={`pokemon-option ${option === focusedOption && 'is-focused'}`}
      style={{ display: 'flex', alignItems: 'center', height: 95, justifyContent: 'space-between' }}
      key={option.value}
      role="presentation"
      onClick={() => selectValue(option)}
      onMouseEnter={() => focusOption(option)}
    >
      <img src={option.sprite} alt={option.label} />
      <span className="pokemon-name">{option.label}</span>
      <span className="pokemon-stats">
        A: {option.attack} | D: {option.defense} | HP: {option.hp}
      </span>
    </div>
  );
};

const PokemonSelector = (props) => {
  const {
    name,
    errors,
    pokemon,
    setFieldValue,
    values,
  } = props;

  const handleSelect = (choice) => {
    setFieldValue(name, choice);
  };

  if (values[name]) {
    return (
      <SelectedPokemonCard
        {...props}
        pokemon={values[name]}
      />
    );
  }

  return (
    <VirtualizedSelect
      className={`pokemon-selector ${errors[name] && 'is-invalid'}`}
      name={name}
      id={name}
      onChange={handleSelect}
      options={pokemon}
      optionHeight={95}
      optionRenderer={PokemonOption}
      value={values[name]}
      valueKey="value"
    />
  );
};

const BattleCreationInnerForm = (props) => {
  const {
    values,
    errors,
    touched,
    handleSubmit,
    isSubmitting,
    setFieldValue,
    users,
  } = props;

  const handleOpponentSelect = (choice) => {
    const value = choice ? choice.value : null;
    setFieldValue('opponent', value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="opponent" >Select your opponent</label>
      <VirtualizedSelect
        id="opponent"
        name="opponent"
        className={`input ${errors.opponent && touched.opponent && 'is-invalid'}`}
        options={users}
        onChange={handleOpponentSelect}
        value={values.opponent}
        placeholder="Find an opponent for you..."
      />
      {touched.opponent && errors.opponent && <div className="form-error">{errors.opponent}</div>}

      <label htmlFor="firstPokemon">Build your team</label>
      <PokemonSelector
        {...props}
        name="firstPokemon"
      />
      <PokemonSelector
        {...props}
        name="secondPokemon"
      />
      <PokemonSelector
        {...props}
        name="thirdPokemon"
      />
      <input type="submit" disabled={isSubmitting} value="Create the battle" />
    </form>
  );
};

const BattleCreationForm = withFormik({
  mapPropsToValues: ({ opponent }) => ({ opponent: opponent || '' }),
  /* eslint-disable no-unused-vars,no-console */
  handleSubmit: (values, { props, setSubmitting, setErrors }) => {
    console.log('Result', values); // wip
  },
  /* eslint-enable */
  validationSchema: Yup.object().shape({
    opponent: Yup.string()
      .nullable()
      .required('Unfortunately, this system isn\'t advanced enough to let you battle with a ghost... Yet. 👻'),
    firstPokemon: Yup.object()
      .nullable()
      .required('You must select at least 3 Pokemon to create a battle'),
    secondPokemon: Yup.object()
      .nullable()
      .required('You must select at least 3 Pokemon to create a battle'),
    thirdPokemon: Yup.object()
      .nullable()
      .required('You must select at least 3 Pokemon to create a battle'),
  }),
})(BattleCreationInnerForm);

class BattleCreate extends React.Component {
  componentDidMount() {
    this.props.loadPokemon();
    this.props.loadUsers();
  }

  render() {
    return (
      <div className="battle-create-container">
        <h2>Create a Battle</h2>
        <BattleCreationForm
          users={this.props.users}
          pokemon={this.props.pokemon}
        />
      </div>
    );
  }
}

BattleCreate.propTypes = {
  loadUsers: PropTypes.func.isRequired,
  loadPokemon: PropTypes.func.isRequired,
  users: PropTypes.arrayOf(PropTypes.object),
  pokemon: PropTypes.arrayOf(PropTypes.object),
};

BattleCreate.defaultProps = {
  users: [],
  pokemon: [],
};

BattleCreationInnerForm.propTypes = {
  errors: PropTypes.shape({
    opponent: PropTypes.string,
  }).isRequired,
  values: PropTypes.shape({
    // On initial state, it's a string. When set, it's a number.
    opponent: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  }).isRequired,
  touched: PropTypes.shape({
    opponent: PropTypes.bool,
  }).isRequired,
  isSubmitting: PropTypes.bool.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  setFieldValue: PropTypes.func.isRequired,
  users: PropTypes.arrayOf(PropTypes.object),
  pokemon: PropTypes.arrayOf(PropTypes.object),
};

BattleCreationInnerForm.defaultProps = {
  // I can't use .isRequired in propTypes otherwise I'll get a error,
  // since it's initially undefined until it loads the users list
  users: [],
  pokemon: [],
};

PokemonOption.propTypes = {
  option: PropTypes.shape(pokemonShape).isRequired,
  selectValue: PropTypes.func.isRequired,
  focusedOption: PropTypes.shape(pokemonShape).isRequired,
  focusOption: PropTypes.func.isRequired,
};

SelectedPokemonCard.propTypes = {
  setFieldValue: PropTypes.func.isRequired,
  pokemon: PropTypes.shape(pokemonShape).isRequired,
  name: PropTypes.string.isRequired,
};

PokemonSelector.propTypes = {
  name: PropTypes.string.isRequired,
  errors: PropTypes.shape({
    opponent: PropTypes.string,
  }).isRequired,
  touched: PropTypes.shape({
    opponent: PropTypes.bool,
  }).isRequired,
  pokemon: PropTypes.arrayOf(PropTypes.shape(pokemonShape)),
  setFieldValue: PropTypes.func.isRequired,
  values: PropTypes.oneOfType([PropTypes.object, PropTypes.array]).isRequired,
};

PokemonSelector.defaultProps = {
  pokemon: [],
};

const mapStateToProps = state => ({
  users: state.user.users,
  pokemon: state.pokemon.list,
});

const mapDispatchToProps = dispatch => ({
  loadUsers: () => dispatch(fetchAndLoadUsers()),
  loadPokemon: () => dispatch(fetchAndLoadPokemonList()),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleCreate);
