import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { selectHydratedBattle } from '../selectors/battle';
import { fetchAndSetBattleList } from '../actions/battleList';
import '../../css/transitions.css';
import Loading from '../components/Loading';
import BattleHelpers from '../utils/battle';
import Urls from '../utils/urls';

const Title = styled.h1`
    text-align: center;
    font-weight: bold;
`;

const WinnerContainer = styled.div`
    justify-content: center;
    align-items: center;
    display: flex;
`;

function PokemonLoading(props) {
  const { currentUserActive, battleId, content } = props;
  if (currentUserActive) {
    return (
      <a href={Urls['battles:team'](battleId)} className="active-build-team">
        <div className="placeholder-card">
          {content}
        </div>
      </a>
    );
  }

  return (
    <div className="placeholder-card">
      {content}
    </div>
  );
}

function PokemonInfoPlaceholder() {
  const repeater = [1, 2, 3];
  return (
    <div>
      {repeater.map(i => (
        <div className="pokemon-card inactive" key={i}>
          <div className="pokemon-pic placeholder-comp" />
          <div className="pokemon-name placeholder-comp" />
          <div className="attributes">
            <span className="placeholder-comp" />
            <span className="placeholder-comp" />
            <span className="placeholder-comp" />
          </div>
        </div>))
      }
    </div>
  );
}

function PokemonInfo(props) {
  return (
    <div className="team-column">
      {props.team.map(pokemon => (
        <div className="pokemon-card" key={pokemon.name}>
          <img alt={pokemon.name} className="picture" src={pokemon.sprite} />
          <div className="name">{pokemon.name}</div>
          <div className="stats">
            <li>Attack: {pokemon.attack}</li>
            <li>Defense: {pokemon.defense}</li>
            <li>HP: {pokemon.hp}</li>
          </div>
        </div>
      ))}
    </div>
  );
}

function TeamDetails(props) {
  const { battle, user, currentUser } = props;
  if (!BattleHelpers.userHasChosenTeam(battle, currentUser)) {
    return <PokemonInfoPlaceholder />;
  }
  return <PokemonInfo team={BattleHelpers.getUserTeam(battle, user)} />;
}

class BattleDetails extends React.Component {
  componentDidMount() {
    const { store, loadBattles } = this.props;
    if (!store.battles) {
      loadBattles();
    }
  }

  getWinnerPosition() {
    const { battle } = this.props;

    if (!battle.winner) {
      return null;
    }
    return battle.winner === battle.creator.username ? 'creator' : 'opponent';
  }

  render() {
    const { user, store, match } = this.props;
    const battleId = this.props.match.params.pk;

    if (!store.battles) {
      return <Loading />;
    }

    const battle = selectHydratedBattle(store.battles[match.params.pk], store);

    const creatorTeam = battle.creator.pokemons;
    const opponentTeam = battle.opponent.pokemons;

    return (
      <div className="battle-container">
        <Title>Battle details</Title>
        <div className="battle-title">
          {battle.creator.trainer.username} vs.
          {battle.opponent.trainer.username}
        </div>
        {battle.winner &&
          <WinnerContainer>
            <div className="battle-winner-label">The winner is {battle.winner.username}</div>
          </WinnerContainer>
        }
        <div
          className={`battle-row ${this.getWinnerPosition()}`}
        >
          {!creatorTeam
            ? <PokemonLoading
              currentUserActive={battle.creator.trainer.username === user.username}
              content={`Waiting for ${battle.creator.trainer.username === user.username ? 'you' : battle.creator.trainer.username} to build the team`}
              battleId={battleId}
            />
            : <TeamDetails
              battle={battle}
              user={battle.creator.trainer}
              currentUser={user}
            />
          }
          {!opponentTeam
            ? <PokemonLoading
              currentUserActive={battle.opponent.trainer.username === user.username}
              content={`Waiting for ${battle.opponent.trainer.username === user.username ? 'you' : battle.opponent.trainer.username} to build the team`}
              battleId={battleId}
            />
            : <TeamDetails
              battle={battle}
              user={battle.opponent.trainer}
              currentUser={user}
            />
          }
        </div>
      </div>
    );
  }
}

BattleDetails.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      pk: PropTypes.string,
    }),
  }).isRequired,
  battle: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
  user: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  store: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  loadBattles: PropTypes.func.isRequired,
};

BattleDetails.defaultProps = {
  battle: {},
  user: {},
};

PokemonLoading.propTypes = {
  content: PropTypes.string.isRequired,
  currentUserActive: PropTypes.bool.isRequired,
  battleId: PropTypes.string.isRequired,
};

TeamDetails.propTypes = {
  battle: PropTypes.shape({
    id: PropTypes.number.isRequired,
    creator: PropTypes.shape({
      trainer: PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
      }),
      pokemons: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        sprite: PropTypes.string,
        attack: PropTypes.number,
        defense: PropTypes.number,
        hp: PropTypes.number,
      })),
    }),
    opponent: PropTypes.shape({
      trainer: PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
      }),
      pokemons: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        sprite: PropTypes.string,
        attack: PropTypes.number,
        defense: PropTypes.number,
        hp: PropTypes.number,
      })),
    }),
  }).isRequired,
  user: PropTypes.shape({
    id: PropTypes.number,
    username: PropTypes.string.isRequired,
  }).isRequired,
  currentUser: PropTypes.shape({
    id: PropTypes.number,
    username: PropTypes.string,
  }).isRequired,
};

TeamDetails.defaultProps = {
  user: {},
  currentUser: {},
};

PokemonInfo.propTypes = {
  team: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    creator: PropTypes.shape({
      username: PropTypes.string.isRequired,
      pokemons: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        sprite: PropTypes.string,
        attack: PropTypes.number,
        defense: PropTypes.number,
        hp: PropTypes.number,
      })),
    }),
    opponent: PropTypes.shape({
      username: PropTypes.string.isRequired,
      pokemons: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        sprite: PropTypes.string,
        attack: PropTypes.number,
        defense: PropTypes.number,
        hp: PropTypes.number,
      })),
    }),
  })).isRequired,
};

const mapStateToProps = state => ({
  store: state.battle,
  user: state.user.details,
});

const mapDispatchToProps = dispatch => ({
  loadBattles: () => dispatch(fetchAndSetBattleList()),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleDetails);

export {
  BattleDetails as NotConnectedBattleDetails,
  PokemonInfo,
};
