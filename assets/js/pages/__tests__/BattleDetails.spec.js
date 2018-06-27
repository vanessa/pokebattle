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
    expect(Component.find('.battle-winner-label')).toHaveLength(0);
  });

  test('finished battle shows the winner label', () => {
    const params = {
      battle: {
        ...battleMock,
        winner: 'vanessa',
      },
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
    expect(Component.state().battle.winner).toBe('vanessa');
    expect(Component.find('.battle-winner-label').text()).toEqual('The winner is vanessa');
    expect(Component.find('.battle-winner-label')).toHaveLength(1);
  });

  test('if user hasn\'t their team, "Build team" link will be showed', () => {
    const params = {
      battle: battleMock,
      user: {
        username: 'vanessa.freitasb',
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
    expect(Component.find('#buildTeamLink')).toHaveLength(1);
  });

  test('if user has built their team, "Build team" link will be hidden', () => {
    const params = {
      battle: battleMock,
      user: {
        username: 'vanessa',
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
    expect(Component.find('#buildTeamLink')).toHaveLength(0);
  });

  test('if opponent has built their team, battle creator cannot see it until they have built too', () => {
    const params = {
      battle: battleMock,
      user: {
        username: 'vanessa.freitasb',
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
    expect(Component.find('.pokemon-card.inactive')).toHaveLength(3);
    expect(Component.find('.placeholder-card')).toHaveLength(1);
  });
});
