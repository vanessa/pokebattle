import React from 'react';
import { mount } from 'enzyme';
import { NotConnectedBattleDetails } from '../BattleDetails';
import battleMock from '../../utils/apiMocks';

jest.mock('../../utils/urls');

describe('BattleDetails', () => {
  let Component;

  test('not finished battle doesn\'t show the winner label', () => {
    const stateParams = {
      user: {
        username: 'test',
        id: 1,
      },
      battleId: 1,
    };
    const propsParams = {
      battle: {
        1: battleMock,
      },
    };
    Component = mount((
      <NotConnectedBattleDetails
        match={{
          params: {
            pk: '1',
          },
        }}
      />
    ));
    Component.setState(stateParams);
    Component.setProps(propsParams);
    expect(Component.props().battle[1].winner).toBeNull();
    expect(Component.contains('WinnerContainer')).toBeFalsy();
    expect(Component.find('.battle-winner-label')).toHaveLength(0);
  });

  test('finished battle shows the winner label', () => {
    const stateParams = {
      user: {
        username: 'test',
        id: 1,
      },
      battleId: 1,
    };
    const propsParams = {
      battle: {
        1: {
          ...battleMock,
          winner: 'vanessa',
        },
      },
    };
    Component = mount((
      <NotConnectedBattleDetails
        match={{
          params: {
            pk: '1',
          },
        }}
      />
    ));
    Component.setState(stateParams);
    Component.setProps(propsParams);
    expect(Component.props().battle[1].winner).toBe('vanessa');
    expect(Component.find('.battle-winner-label').text()).toEqual('The winner is vanessa');
    expect(Component.find('.battle-winner-label')).toHaveLength(1);
  });
});
