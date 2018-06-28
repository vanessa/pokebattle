import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import pokebattleReducer from './reducers';
import App from './App';

const store = createStore(pokebattleReducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('pokebattleContainer'),
);
