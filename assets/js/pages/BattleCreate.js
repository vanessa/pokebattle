import React from 'react';
import PropTypes from 'prop-types';
import { withFormik } from 'formik';
import VirtualizedSelect from 'react-virtualized-select';

import 'react-select/dist/react-select.css';
import 'react-virtualized-select/styles.css';

const imaginaryThings = [
  { label: 'Thing 1', value: 1 },
  { label: 'Thing 2', value: 2 },
  { label: 'Thing 3', value: 3 },
  { label: 'Thing 4', value: 4 },
  { label: 'Thing 5', value: 5 },
];

const BattleCreationInnerForm = (props) => {
  const {
    values,
    errors,
    touched,
    handleSubmit,
    isSubmitting,
    setFieldValue,
  } = props;

  const handleSelect = (choice) => {
    setFieldValue('opponent', choice.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <VirtualizedSelect
        id="opponent"
        className={`input ${errors.opponent && touched.opponent && 'is-invalid'}`}
        name="opponent"
        options={imaginaryThings}
        onChange={handleSelect}
        value={values.opponent}
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

const BattleCreate = () => (
  <div className="battle-create-container">
    <h2>Create a Battle</h2>
    <BattleCreationForm />
  </div>
);

BattleCreationInnerForm.propTypes = {
  errors: PropTypes.shape({
    opponent: PropTypes.string,
  }).isRequired,
  values: PropTypes.shape({
    opponent: PropTypes.number,
  }).isRequired,
  touched: PropTypes.bool.isRequired,
  isSubmitting: PropTypes.bool.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  setFieldValue: PropTypes.func.isRequired,
};

export default BattleCreate;
