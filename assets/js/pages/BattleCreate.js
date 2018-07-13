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
      key={option.id}
      role="presentation"
      onClick={() => selectValue(option.id)}
      onMouseEnter={() => focusOption(option)}
    >
      <img src={option.sprite} alt={option.name} />
      <span className="pokemon-name">{option.name}</span>
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
    touched,
    pokemon,
  } = props;

  const handleSelect = (choice) => {
    /* eslint-disable no-unused-vars,no-console */
    const value = choice ? choice.value : null;
    console.log(choice);  // wip
    /* eslint-enable */
  };

  return (
    <VirtualizedSelect
      className={`pokemon-selector ${errors.pokemon && touched.pokemon && 'is-invalid'}`}
      name={name}
      id={name}
      onChange={handleSelect}
      optionHeight={100}
      optionRenderer={PokemonOption}
      valueComponent={PokemonOption}
      options={pokemon}
      valueKey="id"
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

  const handleSelect = (choice) => {
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
        onChange={handleSelect}
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

PokemonSelector.propTypes = {
  name: PropTypes.string.isRequired,
  errors: PropTypes.shape({
    opponent: PropTypes.string,
  }).isRequired,
  touched: PropTypes.shape({
    opponent: PropTypes.bool,
  }).isRequired,
  pokemon: PropTypes.arrayOf(PropTypes.shape(pokemonShape)),
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
