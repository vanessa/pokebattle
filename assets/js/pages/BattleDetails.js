import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import '../../css/transitions.css';
import Loading from '../components/Loading';
import Api from '../utils/api';
import BattleHelpers from '../utils/battle';
import { capitalizeFirst, Urls } from '../utils';

const Title = styled.h2`
    text-align: center;
    font-weight: bold;
    margin: 30px 0 20px;
    color: #fff;
`;

const BattleTitle = styled.h3`
    text-align: center;
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
        <div
          key={pokemon.name}
          className="battle-pokemon-card"
        >
          <div
            className="pokemon-pic"
            style={{
              backgroundImage: `url(${pokemon.sprite})`,
            }}
          />
          <div className="pokemon-name">
            {capitalizeFirst(pokemon.name)}
            <div className="pokemon-health-bar" />
            <div className="pokemon-health">HP{pokemon.hp}/{pokemon.hp}</div>
          </div>
          <div className="pokemon-stats">
            <li>
              <span className="value">{pokemon.attack}</span>
              <span className="stat-name">Attack</span>
            </li>
            <li>
              <span className="value">{pokemon.defense}</span>
              <span className="stat-name">Defense</span>
            </li>
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
  constructor(props) {
    super(props);

    this.state = {
      battle: null,
    };
  }

  componentDidMount() {
    const battleId = this.props.match.params.pk;
    Api.getBattleDetails(battleId)
      .then((battle) => {
        this.setState({
          battle,
        });
      });
    Api.getUserInfo()
      .then((user) => {
        this.setState({
          user,
        });
      });
  }

  getWinnerPosition() {
    const battle = this.state.battle;
    if (!battle.winner) {
      return null;
    }
    return battle.winner === battle.creator.username ? 'creator' : 'opponent';
  }


  render() {
    const { battle, user } = this.state;

    if (battle) {
      const creatorTeam = battle.creator.pokemons;
      const opponentTeam = battle.opponent.pokemons;
      const battleId = this.props.match.params.pk;

      return (
        <div className="battle-details">
          <Title>Battle details</Title>

          <div className="battle-details-container">
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
          </div>
        </div>
      );
    }
    return <Loading />;
  }
}

BattleDetails.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      pk: PropTypes.string,
    }),
  }).isRequired,
};

PokemonLoading.propTypes = {
  content: PropTypes.string.isRequired,
  battleId: PropTypes.string.isRequired,
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
    id: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
  }).isRequired,
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

export {
  BattleDetails,
  PokemonInfo,
};
