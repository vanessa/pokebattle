import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { withFormik } from 'formik';
import VirtualizedSelect from 'react-virtualized-select';
import 'react-select/dist/react-select.css';
import 'react-virtualized-select/styles.css';
import fetchAndLoadUsers from '../actions/users';

const BattleCreationInnerForm = (props) => {
  const {
    values,
    errors,
    touched,
    handleSubmit,
    isSubmitting,
    setFieldValue,
    users,
  } = props;

  const handleSelect = (choice) => {
    const value = choice ? choice.value : null;
    setFieldValue('opponent', value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <VirtualizedSelect
        id="opponent"
        className={`input ${errors.opponent && touched.opponent && 'is-invalid'}`}
        name="opponent"
        options={users}
        onChange={handleSelect}
        value={values.opponent}
        placeholder="Find an opponent for you..."
      />
      {touched.email && errors.email && <div>{errors.email}</div>}
      <button type="submit" disabled={isSubmitting}>
        Create the battle
      </button>
    </form>
  );
};

const BattleCreationForm = withFormik({
  mapPropsToValues: ({ opponent }) => ({ opponent: opponent || '' }),
  /* eslint-disable no-unused-vars,no-console */
  handleSubmit: (values, { props, setSubmitting, setErrors }) => {
    console.log('Result', values); // wip
  },
  /* eslint-enable */
})(BattleCreationInnerForm);

class BattleCreate extends React.Component {
  componentDidMount() {
    this.props.loadUsers();
  }

  render() {
    return (
      <div className="battle-create-container">
        <h2>Create a Battle</h2>
        <BattleCreationForm users={this.props.users} />
      </div>
    );
  }
}

BattleCreate.propTypes = {
  loadUsers: PropTypes.func.isRequired,
  users: PropTypes.arrayOf(PropTypes.object),
};

BattleCreate.defaultProps = {
  users: [],
};

BattleCreationInnerForm.propTypes = {
  errors: PropTypes.shape({
    opponent: PropTypes.string,
  }).isRequired,
  values: PropTypes.shape({
    // On initial state, it's a string. When set, it's a number.
    opponent: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  }).isRequired,
  touched: PropTypes.shape({
    opponent: PropTypes.bool,
  }).isRequired,
  isSubmitting: PropTypes.bool.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  setFieldValue: PropTypes.func.isRequired,
  users: PropTypes.arrayOf(PropTypes.object),
};

BattleCreationInnerForm.defaultProps = {
  // I can't use .isRequired in propTypes otherwise I'll get a error,
  // since it's initially undefined until it loads the users list
  users: [],
};

const mapStateToProps = state => ({
  users: state.user.users,
});

const mapDispatchToProps = dispatch => ({
  loadUsers: () => dispatch(fetchAndLoadUsers()),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(BattleCreate);
