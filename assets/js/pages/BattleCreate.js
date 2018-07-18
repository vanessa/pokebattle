import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import VirtualizedSelect from 'react-virtualized-select';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import 'react-select/dist/react-select.css';
import 'react-virtualized-select/styles.css';
import { reorder } from '../utils';
import fetchAndLoadPokemonList from '../actions/pokemon';
import fetchAndLoadUsers from '../actions/users';
import { pokemonShape } from '../utils/propTypes';
import TimesIcon from '../../images/icons/times.svg';

function indexHelper(name) {
  switch (name) {
    // return the index
    case 'firstPokemon':
      return 0;
    case 'secondPokemon':
      return 1;
    case 'thirdPokemon':
      return 2;
    default:
      return null;
  }
}

const SelectedPokemonCard = (props) => {
  const { pokemon, setFieldValue, name, isDragging } = props;
  const index = indexHelper(name);

  const clearSelection = () => {
    setFieldValue(`team.${index}`, null);
  };

  return (
    <div className={`pokemon-chosen-card ${isDragging ? 'is-dragging' : ''}`}>
      <img src={pokemon.sprite} alt={pokemon.label} />
      <div className="pokemon-name">{pokemon.label}</div>
      <div className="pokemon-stats">
        A: {pokemon.attack} | D: {pokemon.defense} | HP: {pokemon.hp}
      </div>
      <div
        className="clear-pokemon"
        role="presentation"
        onClick={clearSelection}
      >
        <img src={TimesIcon} alt="Clear selection" width="30" />
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
    style,
  } = props;

  return (
    <div
      className={`pokemon-option ${option === focusedOption && 'is-focused'}`}
      style={style}
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

  const index = indexHelper(name);

  const handleSelect = (choice) => {
    setFieldValue(`team.${index}`, choice);
  };

  if (values.team[index]) {
    return (
      <Draggable key={name} draggableId={name} index={index}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}
          >
            <SelectedPokemonCard
              {...props}
              pokemon={values.team[index]}
              isDragging={snapshot.isDragging}
            />
            {provided.placeholder}
          </div>
        )}
      </Draggable>
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

  const onDragEnd = (result) => {
    if (!result.destination) {
      return;
    }

    const items = reorder(
      values.team,
      result.source.index,
      result.destination.index,
    );

    setFieldValue('team', items);
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
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
        <Droppable droppableId="pokemonList">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              className={snapshot.isDraggingOver ? 'dragging-zone' : ''}
            >
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
            </div>
          )}
        </Droppable>
        <input type="submit" disabled={isSubmitting} value="Create the battle" />
      </form>
    </DragDropContext>
  );
};

const BattleCreationForm = withFormik({
  mapPropsToValues: ({ opponent, firstPokemon, secondPokemon, thirdPokemon }) => ({
    opponent: opponent || '',
    team: [firstPokemon, secondPokemon, thirdPokemon],
  }),
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
  style: PropTypes.oneOfType([PropTypes.array, PropTypes.object]).isRequired,
};

SelectedPokemonCard.propTypes = {
  setFieldValue: PropTypes.func.isRequired,
  pokemon: PropTypes.shape(pokemonShape).isRequired,
  name: PropTypes.string.isRequired,
  isDragging: PropTypes.bool.isRequired,
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
