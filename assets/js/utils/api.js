import axios from 'axios';
import Urls from './urls';

const getCookie = (name) => {
  const b = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return b ? b.pop() : '';
};

const pokeWrapper = axios.create({
  params: {
    session: getCookie('sessionid'),
  },
});

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return pokeWrapper.get(url)
      .then(response => response.data);
  }

  static getUserInfo() {
    const url = Urls['api-users:user-details']();
    return pokeWrapper.get(url)
      .then(response => response.data);
  }
}
