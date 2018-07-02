import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import battleList from '../mocks/battlesMocks';
import Urls from '../utils/urls';

const BattleLabel = ({ battle }) => {
  // Had to use snake case here due to API response
  const { status, status_label } = battle;

  // Transform to string because for some reason it's not originally
  const StatusLabel = String(status_label);

  let labelColor;

  switch (status) {
    case 'F':
      labelColor = 'battle-finished';
      break;
    case 'P':
      labelColor = 'processing';
      break;
    default:
      labelColor = 'ongoing';
  }

  const label = {
    class: `label ${labelColor}`,
    displayText: StatusLabel.charAt(0).toUpperCase() + StatusLabel.substring(1),
  };

  return (
    <div className={label.class}>
      {label.displayText}
    </div>
  );
};

const BattlesColumn = ({ title }) => (
  <div className="battles-grid-column">
    <h3>{title}</h3>
    <div className="battle-list">
      {
        battleList.map(battle => (
          <Link
            key={battle.id}
            to={Urls['battles:details'](battle.id)}
            className="battle-item"
          >
            <div className="battle-id">{battle.id}</div>
            {battle.creator.username} vs {battle.opponent.username}
            <BattleLabel
              battle={battle}
            />
          </Link>
        ),
        )
      }
    </div>
  </div>
);

const BattleList = () => (
  <div className="battle-list-container">
    <h2>My battles</h2>
    <div className="battles-grid">
      <BattlesColumn
        title="Battles you created"
      />
      <BattlesColumn
        title="Battles you were invited"
      />
    </div>
  </div>
);

BattlesColumn.propTypes = {
  title: PropTypes.string,
};

BattlesColumn.defaultProps = {
  title: '',
};

BattleLabel.propTypes = {
  battle: PropTypes.object.isRequired, // eslint-disable-line react/forbid-prop-types
};

export default BattleList;
