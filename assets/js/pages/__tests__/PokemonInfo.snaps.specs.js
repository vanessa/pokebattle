import React from 'react';
import renderer from 'react-test-renderer';
import { PokemonInfo } from '../BattleDetails';

describe('PokemonInfo', () => {
  let Component;
  let tree;
  const team = [
    {
      id: 1,
      name: 'Test Pokemon',
      sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
      attack: 2,
      defense: 2,
      hp: 2,
    },
  ];

  test('renders', () => {
    Component = renderer.create((
      <PokemonInfo
        team={team}
      />
    ));

    tree = Component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
