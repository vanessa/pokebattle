import React from 'react';
import { mount } from 'enzyme';
import { BattleDetails } from '../BattleDetails';
import battleMock from '../__mocks__/BattleDetails';

jest.mock('../../utils/urls');

describe('BattleDetails', () => {
  let Component;

  test('not finished battle doesn\'t show the winner label', () => {
    const params = {
      battle: battleMock,
      user: {
        username: 'test',
        id: 1,
      },
    };
    Component = mount((
      <BattleDetails
        match={{
          params: {
            pk: '1',
          },
        }}
      />
    ));
    Component.setState(params);
    expect(Component.state().battle.winner).toBeNull();
    expect(Component.contains('WinnerContainer')).toBeFalsy();
  });
});
