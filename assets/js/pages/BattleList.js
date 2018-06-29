import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import battleList from '../mocks/battlesMocks';
import Urls from '../utils/urls';

const BattleLabel = ({ status }) => <div className="battle-label">{status}</div>;

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
            <BattleLabel status={battle.status} />
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
  status: PropTypes.string.isRequired,
};

export default BattleList;
