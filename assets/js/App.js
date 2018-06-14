import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import BattleDetails from './pages/BattleDetails';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Navbar />
        <Switch>
          <Route path="/battles/details/:pk" component={BattleDetails} />
          <Route render={() => <p>Not found!</p>} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
