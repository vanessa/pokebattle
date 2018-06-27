import React from 'react';
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
          <a href={Urls['battles:list']()}>
            My battles
          </a>
          <a href={Urls['battles:create-battle']()}>
            Battle
          </a>
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
