import axios from 'axios';
import Urls from './urls';

const getCookie = (name) => {
  const b = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return b ? b.pop() : '';
};

const pokeWrapper = axios.create({
  params: {
    session_id: getCookie('sessionid'),
  },
});

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return pokeWrapper.get(url)
      .then(response => response.data)
      .then(data => data);
  }
}
