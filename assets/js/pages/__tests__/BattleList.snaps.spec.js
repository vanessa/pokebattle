import React from 'react';
import renderer from 'react-test-renderer';
import { NotConnectedBattleList } from '../BattleList';

jest.mock('../../utils/urls');

describe('BattleList', () => {
  let Component;
  let tree;

  it('renders', () => {
    Component = renderer.create((
      <NotConnectedBattleList
        loadBattleList={jest.fn()}
      />
    ));

    tree = Component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
