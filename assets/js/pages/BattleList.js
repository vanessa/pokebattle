import React from 'react';
import PropTypes from 'prop-types';

const BattlesColumn = ({ title }) => (
  <div className="battles-grid-column">
    <h3>{title}</h3>
    <div className="battle-list">
      {
        [1, 2, 3, 4].map(battle => <div key={battle}>{battle}</div>)
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

export default BattleList;
