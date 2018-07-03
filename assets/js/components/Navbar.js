import React from 'react';
import { NavLink } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Urls from '../utils/urls';

const Navbar = ({ user }) => (
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
        to={Urls['battles:create-battle']()}
      >
        Create a battle
      </NavLink>
      <a href={Urls['battles:invite']()}>
        Invite someone
      </a>
      <span>
        {
          user &&
          <span>Hello, <b>{user.username}</b>!</span>
        }
      </span>
      <a href={Urls['auth:logout']()}>
        Logout
      </a>
    </div>
  </div>
);

Navbar.propTypes = {
  user: PropTypes.oneOfType([
    PropTypes.object,
    PropTypes.array,
  ]),
};

Navbar.defaultProps = {
  user: {},
};

const mapStateToProps = state => ({
  user: state.user.details,
});

export default connect(
  mapStateToProps,
  null,
)(Navbar);
