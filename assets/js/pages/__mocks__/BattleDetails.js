const battleMock = {
  id: 14,
  creator: {
    pokemons: [
      {
        id: 1,
        name: 'bulbasaur',
        sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
        attack: 49,
        defense: 49,
        hp: 45,
      },
      {
        id: 2,
        name: 'ivysaur',
        sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png',
        attack: 62,
        defense: 63,
        hp: 60,
      },
      {
        id: 5,
        name: 'charmeleon',
        sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png',
        attack: 64,
        defense: 58,
        hp: 58,
      },
    ],
    username: 'vanessa',
  },
  opponent: {
    username: 'vanessa.freitasb',
  },
  winner: null,
  date_created: '2018-06-14T22:49:10.648928Z',
  status: 'O',
};

export default battleMock;
