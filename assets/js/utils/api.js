import Urls from './urls';

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return fetch(url)
      .then(response => response.json())
      .then(data => data);
  }
}
