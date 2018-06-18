import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import BattleDetails from './pages/BattleDetails';
import Login from './pages/Login';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Navbar />
        <Switch>
          <Route path="/battles/details/:pk" component={BattleDetails} />
          <Route path="/login" component={Login} />
          <Route render={() => <p>Not found!</p>} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
