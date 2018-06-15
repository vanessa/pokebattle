import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import '../../css/transitions.css';
import Loading from '../components/Loading';
import Api from '../utils/api';

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
  return (
    <div className="placeholder-card">
      {props.content}
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
  const battleFinished = props.battleStatus === 'F';
  const { team } = props;

  if (!battleFinished) {
    return <PokemonInfoPlaceholder />;
  }
  return <PokemonInfo team={team} />;
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
  }

  getWinnerPosition() {
    const battle = this.state.battle;
    if (!battle.winner) {
      return null;
    }
    return battle.winner === battle.creator.username ? 'creator' : 'opponent';
  }


  render() {
    const { battle } = this.state;

    if (battle) {
      const creatorTeam = battle.creator.pokemons;
      const opponentTeam = battle.opponent.pokemons;
      const battleId = this.props.match.params.pk;

      return (
        <Container>
          <Title>Battle details</Title>
          <BattleTitle>{battle.creator.username} vs. {battle.opponent.username}</BattleTitle>
          {!battle.winner &&
            <a
              style={{ textAlign: 'center', display: 'block' }}
              href={window.Urls['battles:team'](battleId)}
            >
              Choose team
            </a>
          }
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
                content={`Waiting for ${battle.creator.username} to choose their team`}
              />
              : <TeamDetails
                battleStatus={battle.status}
                team={creatorTeam}
              />
            }
            {!opponentTeam
              ? <PokemonLoading
                content={`Waiting for ${battle.opponent.username} to choose their team`}
              />
              : <TeamDetails
                battleStatus={battle.status}
                team={opponentTeam}
              />
            }
          </div>
        </Container>
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
};

TeamDetails.propTypes = {
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
  battleStatus: PropTypes.string.isRequired,
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

export default BattleDetails;
