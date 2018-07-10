import Urls from './urls';

function isEmpty(obj) {
  if (!Object.prototype.hasOwnProperty.call(obj, 'id')) {
    return false;
  }
  return true;
}

export {
  Urls,
  isEmpty,
};
