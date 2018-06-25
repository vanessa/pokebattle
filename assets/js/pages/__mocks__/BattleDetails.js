const battleMock = {
  pk: 2,
  creator: 'Vanessa',
  opponent: 'Amanda',
  winner: 'Vanessa',
};

const creatorPokemonTeam = {
  battle_related: 'Vanessa vs. Amanda',
  trainer: 'Vanessa',
  pokemons: [
    {
      pk: 517,
      name: 'munna',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/517.png',
      attack: 55,
      defense: 45,
      hp: 76,
    },
    {
      pk: 1,
      name: 'bulbasaur',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
      attack: 49,
      defense: 49,
      hp: 45,
    },
    {
      pk: 4,
      name: 'charmander',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',
      attack: 52,
      defense: 43,
      hp: 39,
    },
  ],
};

const opponentPokemonTeam = {
  battle_related: 'Vanessa vs. Amanda',
  trainer: 'Amanda',
  pokemons: [
    {
      pk: 506,
      name: 'lillipup',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/506.png',
      attack: 25,
      defense: 45,
      hp: 76,
    },
    {
      pk: 516,
      name: 'simipour',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/516.png',
      attack: 98,
      defense: 63,
      hp: 75,
    },
    {
      pk: 312,
      name: 'minun',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/312.png',
      attack: 40,
      defense: 50,
      hp: 60,
    },
  ],
};

export {
  battleMock,
  creatorPokemonTeam,
  opponentPokemonTeam,
};
