import React from 'react';
import Urls from '../utils/urls';
// import { NavLink } from 'react-router-dom';

function Navbar() {
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
        <a href={Urls['auth:logout']()}>
          Logout
        </a>
      </div>
    </div>
  );
}

export default Navbar;
