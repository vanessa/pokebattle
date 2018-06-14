import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

const LoadingComponent = styled.div`
    text-align: center;
    font-size: 35px;
    color: #666;
    margin: 50px 0;
`;

class Loading extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      text: props.text,
    };
  }

  componentDidMount() {
    const stopper = `${this.props.text}...`;
    this.interval = window.setInterval(() => {
      if (this.state.text === stopper) {
        this.setState(() => ({
          text: this.props.text,
        }));
      } else {
        this.setState(prevState => ({
          text: `${prevState.text}.`,
        }));
      }
    }, this.props.speed);
  }

  componentWillUnmount() {
    window.clearInterval(this.interval);
  }

  render() {
    return (
      <LoadingComponent>
        {this.state.text}
      </LoadingComponent>
    );
  }
}

Loading.propTypes = {
  text: PropTypes.string.isRequired,
  speed: PropTypes.number.isRequired,
};

Loading.defaultProps = {
  text: 'Loading',
  speed: 300,
};

export default Loading;
