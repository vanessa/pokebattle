import React from 'react';
import renderer from 'react-test-renderer';
import Placeholder from '../Placeholder';

describe('Placeholder', () => {
  let Component;
  let tree;

  test('renders', () => {
    Component = renderer.create((
      <Placeholder />
    ));

    tree = Component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
