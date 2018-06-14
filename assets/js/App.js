import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import styled from 'styled-components';
import Navbar from './components/Navbar';
import BattleDetails from './pages/BattleDetails';


const Container = styled.div`
    padding: 10px;
`;

function App() {
  return (
    <BrowserRouter>
      <Container>
        <Navbar />
        <Switch>
          <Route path="/battles/details/:pk" component={BattleDetails} />
          <Route render={() => <p>Not found!</p>} />
        </Switch>
      </Container>
    </BrowserRouter>
  );
}

export default App;
