import { NavLink } from 'react-router-dom';
import React from 'react';

function Navbar() {
  return (
    <div>
      <NavLink exact to="/" activeClassName="active">Home</NavLink>
      <NavLink exact to="/battles" activeClassName="active">Battles</NavLink>
    </div>
  );
}

export default Navbar;
