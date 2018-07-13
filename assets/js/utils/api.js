import axios from 'axios';
import Urls from './urls';

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return axios.get(url)
      .then(response => response.data)
      .catch(err => new Error(err));
  }

  static getBattleList() {
    const url = Urls['api-battles:battle-list']();
    return axios.get(url)
      .then(response => response.data)
      .catch(err => new Error(err));
  }

  static getUserInfo() {
    const url = Urls['api-users:user-details']();
    return axios.get(url)
      .then(response => response.data)
      .catch(err => new Error(err));
  }

  static loadUsers() {
    const url = Urls['api-users:users']();
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }
}
