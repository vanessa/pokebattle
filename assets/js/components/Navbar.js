import { NavLink } from 'react-router-dom';
import React from 'react';

function Navbar() {
  // Change from 'a' to NavLink according to refactoring
  return (
    <div className="navbar">
      <NavLink exact to="/" activeClassName="active">Home</NavLink>
      <a href={window.Urls['battles:list']()}>Battles</a>
      <a href={window.Urls['battles:create-battle']()}>Battle with someone!</a>
      <a href={window.Urls['battles:invite']()}>Invite someone</a>
      {/* <NavLink exact to="/battles" activeClassName="active">Battles</NavLink> */}
    </div>
  );
}

export default Navbar;
