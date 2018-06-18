import React from 'react';
import PropTypes from 'prop-types';
import Api from '../utils/api';

const Input = ({ type, name }) => (<input
  type={type}
  name={name}
  className={`${name}-input`}
/>);

Input.propTypes = {
  type: PropTypes.string,
  name: PropTypes.string.isRequired,
};

Input.defaultProps = {
  type: 'text',
  name: undefined,
};

class Login extends React.Component {
  state = {
    username: '',
    password: '',
  }

  handleSubmit = (event) => {
    event.preventDefault();
    const username = event.target.username.value;
    const password = event.target.password.value;
    Api.loginUser(username, password);
  }

  render() {
    return (
      <form
        className="login-form"
        onSubmit={this.handleSubmit}
      >
        <Input
          name="username"
        />
        <Input
          type="password"
          name="password"
        />
        <input
          className="submit-button"
          type="submit"
        />
      </form>
    );
  }
}

export default Login;
