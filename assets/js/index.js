import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import { createStore, applyMiddleware } from 'redux';
import pokebattleReducer from './reducers';
import App from './App';

/* eslint-disable no-underscore-dangle */
const store = createStore(
  pokebattleReducer, /* preloadedState, */
  (process.env.NODE_ENV !== 'production' &&
   window.__REDUX_DEVTOOLS_EXTENSION__) &&
   window.__REDUX_DEVTOOLS_EXTENSION__(),
  applyMiddleware(thunk),
);
/* eslint-enable */

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('pokebattleContainer'),
);
