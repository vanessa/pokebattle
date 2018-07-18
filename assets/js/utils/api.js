import axios from 'axios';
import { getCookieValue, Urls } from '.';

const apiWrapper = axios.create({
  headers: { 'X-CSRFToken': getCookieValue('csrftoken') },
});

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }

  static getBattleList() {
    const url = Urls['api-battles:battle-list']();
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }

  static getUserInfo() {
    const url = Urls['api-users:user-details']();
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }

  static loadUsers() {
    const url = Urls['api-users:users']();
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }

  static loadPokemonList() {
    const url = Urls['api-pokemon:list']();
    return axios.get(url)
      .then(response => response.data)
      .catch(error => new Error(error));
  }

  static createBattle(values) {
    const url = Urls['api-battles:create-battle']();
    return apiWrapper.post(url, values)
      .then(response => response.data)
      .catch(error => new Error(error));
  }
}
