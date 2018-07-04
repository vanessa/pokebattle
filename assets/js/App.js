import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { fetchAndSetUserDetails } from './actions/userDetails';
import Navbar from './components/Navbar';
import BattleDetails from './pages/BattleDetails';
import BattleList from './pages/BattleList';
import BattleCreate from './pages/BattleCreate';

class App extends React.Component {
  componentDidMount() {
    this.props.loadUserInfo();
  }

  render() {
    return (
      <BrowserRouter>
        <div>
          <Navbar />
          <Switch>
            <Route path="/battles/details/:pk" component={BattleDetails} />
            <Route exact path="/battles/" component={BattleList} />
            <Route path="/battles/create/" component={BattleCreate} />
            <Route render={() => <p>Not found!</p>} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

App.propTypes = {
  loadUserInfo: PropTypes.func.isRequired,
};

const mapDispatchToProps = dispatch => ({
  loadUserInfo: () => dispatch(fetchAndSetUserDetails()),
});

export default connect(
  null,
  mapDispatchToProps,
)(App);
