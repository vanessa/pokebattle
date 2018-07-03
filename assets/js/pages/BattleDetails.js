import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { fetchAndSetBattleDetails } from '../actions/battleDetails';
import '../../css/transitions.css';
import Loading from '../components/Loading';
import BattleHelpers from '../utils/battle';
import Urls from '../utils/urls';

const Title = styled.h1`
    text-align: center;
    font-weight: bold;
`;

const Container = styled.div`
    padding: 15px;
`;

const BattleTitle = styled.h3`
    text-align: center;
`;

const PokemonCard = styled.div`
    width: 350px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    padding: 15px;
    border-radius: 5px;
    transition: box-shadow .1s ease-in-out;
    cursor: pointer;
    margin: 10px 50px;
`;

const PokemonName = styled.div`
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
    display: block;
    position: relative;
`;

const PokemonPic = styled.img`
    width: 90px;
`;

const PokemonStats = styled.ul`
    list-style-type: none;
    font-size: .8em;
    padding: 0;
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
        <PokemonCard key={pokemon.name}>
          <PokemonPic src={pokemon.sprite} />
          <PokemonName>{pokemon.name}</PokemonName>
          <PokemonStats>
            <li>Attack: {pokemon.attack}</li>
            <li>Defense: {pokemon.defense}</li>
            <li>HP: {pokemon.hp}</li>
          </PokemonStats>
        </PokemonCard>
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
    const battleId = this.props.match.params.pk;
    this.props.loadBattle(battleId);
  }

  getWinnerPosition() {
    const battleId = this.props.match.params.pk;
    const battle = this.props.battle[battleId];

    if (!battle.winner) {
      return null;
    }
    return battle.winner === battle.creator.username ? 'creator' : 'opponent';
  }

  render() {
    const { user } = this.props;
    const battleId = this.props.match.params.pk;
    const battle = this.props.battle[battleId];

    if (!battle) {
      return <Loading />;
    }

    const creatorTeam = battle.creator.pokemons;
    const opponentTeam = battle.opponent.pokemons;

    return (
      <Container>
        <Title>Battle details</Title>
        <BattleTitle>{battle.creator.username} vs. {battle.opponent.username}</BattleTitle>
        {battle.winner &&
          <WinnerContainer>
            <div className="battle-winner-label">The winner is {battle.winner}</div>
          </WinnerContainer>
        }
        <div
          className={`battle-row ${this.getWinnerPosition()}`}
        >
          {!creatorTeam
            ? <PokemonLoading
              battleId={battleId}
              currentUserActive={battle.creator.username === user.username}
              content={`Waiting for ${battle.creator.username === user.username ? 'you' : battle.creator.username} to build the team`}
            />
            : <TeamDetails
              battle={battle}
              user={battle.creator}
              currentUser={user}
            />
          }
          {!opponentTeam
            ? <PokemonLoading
              battleId={battleId}
              currentUserActive={battle.opponent.username === user.username}
              content={`Waiting for ${battle.opponent.username === user.username ? 'you' : battle.opponent.username} to build the team`}
            />
            : <TeamDetails
              battle={battle}
              user={battle.opponent}
              currentUser={user}
            />
          }
        </div>
      </Container>
    );
  }
}

BattleDetails.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      pk: PropTypes.string,
    }),
  }).isRequired,
  loadBattle: PropTypes.func.isRequired,
  battle: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
  user: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]).isRequired,
};

BattleDetails.defaultProps = {
  battle: {},
  loadBattle: () => {},
  user: {},
};

PokemonLoading.propTypes = {
  content: PropTypes.string.isRequired,
  battleId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  currentUserActive: PropTypes.bool.isRequired,
};

TeamDetails.propTypes = {
  battle: PropTypes.shape({
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

const mapDispatchToProps = dispatch => ({
  loadBattle: battleId => dispatch(fetchAndSetBattleDetails(battleId)),
});

const mapStateToProps = state => ({
  battle: state.battle,
  user: state.user.details,
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleDetails);

export {
  BattleDetails as NotConnectedBattleDetails,
  PokemonInfo,
};
