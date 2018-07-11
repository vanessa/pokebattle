import React from 'react';
import { NavLink } from 'react-router-dom';
import Urls from '../utils/urls';
import Api from '../utils/api';

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
    };
  }

  componentDidMount() {
    Api.getUserInfo()
      .then((response) => {
        this.setState({
          username: response.username,
        });
      });
  }

  render() {
    const { username } = this.state;

    return (
      <div className="navbar">
        <div className="header">
          <a href={Urls.home()}>PokeBattle</a>
        </div>
        <div className="menu">
          <NavLink
            to={Urls['battles:list']()}
          >
            My battles
          </NavLink>
          <NavLink
            to="/battles/create"
          >
            Create a battle
          </NavLink>
          <a href={Urls['battles:invite']()}>
            Invite someone
          </a>
          <span>
            {username &&
              `Hello, ${username}!`}
          </span>
          <a href={Urls['auth:logout']()}>
            Logout
          </a>
        </div>
      </div>
    );
  }
}

export default Navbar;
