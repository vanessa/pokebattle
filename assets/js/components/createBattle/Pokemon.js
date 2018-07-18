import React from 'react';
import PropTypes from 'prop-types';
import { Draggable } from 'react-beautiful-dnd';
import VirtualizedSelect from 'react-virtualized-select';
import { indexHelper } from '../../utils';
import TimesIcon from '../../../images/icons/times.svg';
import { pokemonShape } from '../../utils/propTypes';

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

export default PokemonSelector;
