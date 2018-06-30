import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import { BattleDetails } from './pages/BattleDetails';
import BattleList from './pages/BattleList';
import BattleCreate from './pages/BattleCreate';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Navbar />
        <Switch>
          <Route exact path="/battles" activeClassName="navlink-active" component={BattleList} />
          <Route
            path="/battles/details/:pk"
            activeClassName="navlink-active"
            component={BattleDetails}
          />
          <Route
            path="/battles/create"
            activeClassName="navlink-active"
            component={BattleCreate}
          />
          <Route render={() => <p>Not found!</p>} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
