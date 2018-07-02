import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import Loading from '../components/Loading';
import battleSetList from '../actions/battleList';
import Urls from '../utils/urls';
import Api from '../utils/api';

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

const BattlesColumn = ({ title, battles }) => (
  <div className="battles-grid-column">
    <h3>{title}</h3>
    <div className="battle-list">
      {!battles
      ? <Loading />
      : battles.map(battle => (
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

class BattleList extends React.Component {
  componentDidMount() {
    Api.getBattleList()
    .then(list => this.props.loadBattleList(list));
  }

  render() {
    const { battles } = this.props;

    if (!battles) {
      return <Loading />;
    }

    const createdBattles = battles.filter(battle => battle.is_creator);
    const invitedBattles = battles.filter(battle => !battle.is_creator);

    return (
      <div className="battle-list-container">
        <h2>My battles</h2>
        <div className="battles-grid">
          <BattlesColumn
            battles={createdBattles}
            title="Battles you created"
          />
          <BattlesColumn
            battles={invitedBattles}
            title="Battles you were invited"
          />
        </div>
      </div>
    );
  }
}

BattlesColumn.propTypes = {
  title: PropTypes.string,
  battles: PropTypes.arrayOf(PropTypes.object),
};

BattlesColumn.defaultProps = {
  title: '',
  battles: null,
};

BattleLabel.propTypes = {
  battle: PropTypes.object.isRequired, // eslint-disable-line react/forbid-prop-types
};

BattleList.propTypes = {
  loadBattleList: PropTypes.func.isRequired,
  battles: PropTypes.arrayOf(PropTypes.object),
};

BattleList.defaultProps = {
  battles: null,
};

const mapDispatchToProps = dispatch => ({
  loadBattleList: battle => dispatch(battleSetList(battle)),
});

const mapStateToProps = state => ({
  battles: state.battle.battleList,
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleList);

export {
  BattleList as NotConnectedBattleList,
};
