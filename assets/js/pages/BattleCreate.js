import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import VirtualizedSelect from 'react-virtualized-select';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import 'react-select/dist/react-select.css';
import 'react-virtualized-select/styles.css';
import { reorder } from '../utils';
import Api from '../utils/api';
import fetchAndLoadPokemonList from '../actions/pokemon';
import fetchAndLoadUsers from '../actions/users';
import PokemonSelector from '../components/createBattle/Pokemon';

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
              className={`dragging-zone ${snapshot.isDraggingOver ? 'is-dragging' : ''}`}
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
    opponent: opponent || null,
    team: [firstPokemon || null, secondPokemon || null, thirdPokemon || null],
  }),
  handleSubmit: (values, { setSubmitting }) => {
    console.log(values);  // eslint-disable-line
    Api.createBattle(values)
      .then(setSubmitting(false));
  },
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
