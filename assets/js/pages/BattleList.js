import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import Loading from '../components/Loading';
import { fetchAndSetBattleList } from '../actions/battleList';
import { clearCurrentBattle } from '../actions/battleDetails';

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
      {
        battles.map(battle => (
          <Link
            key={battle.id}
            to={`/battles/details/${battle.id}`}
            className="battle-item"
          >
            <div className="battle-id">{battle.id}</div>
            {battle.creator.trainer} vs {battle.opponent.trainer}
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
    this.props.loadBattleList();
    this.props.clearCurrentBattle();
  }

  render() {
    const { battles, result } = this.props;

    if (!battles) {
      return <Loading />;
    }

    const createdBattles = result.map(index => battles[index]).filter(battle => battle.is_creator);
    const invitedBattles = result.map(index => battles[index]).filter(battle => !battle.is_creator);

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
  battles: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
};

BattlesColumn.defaultProps = {
  title: '',
  battles: null,
};

BattleLabel.propTypes = {
  battle: PropTypes.object.isRequired, // eslint-disable-line react/forbid-prop-types
};

BattleList.propTypes = {
  loadBattleList: PropTypes.func,
  clearCurrentBattle: PropTypes.func,
  battles: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
  result: PropTypes.arrayOf(PropTypes.number),
};

BattleList.defaultProps = {
  loadBattleList: null,
  clearCurrentBattle: null,
  battles: null,
  result: [],
};

const mapDispatchToProps = dispatch => ({
  loadBattleList: () => dispatch(fetchAndSetBattleList()),
  clearCurrentBattle: () => dispatch(clearCurrentBattle()),
});

const mapStateToProps = state => ({
  battles: state.battle.battles,
  result: state.battle.result,
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleList);

export {
  BattleList as NotConnectedBattleList,
};
