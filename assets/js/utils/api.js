import axios from 'axios';
import Urls from './urls';

const getToken = () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    throw new Error('Token wasn\'t properly set. Try logging in.');
  }
  return token;
};

const pokeWrapper = axios.create({
  headers: {
    Authorization: `Token ${getToken()}`,
  },
});

export default class Api {
  static getBattleDetails(id) {
    const url = Urls['api-battles:battle-details'](id);
    return pokeWrapper.get(url)
      .then(response => response.data)
      .then(data => data);
  }

  static loginUser(username, password) {
    const url = Urls['obtain-auth-token']();
    return axios.post(url, {
      username,
      password,
    })
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem('authToken', response.data.token);
        }
      })
      .catch((error) => {
        throw new Error(error);
      });
  }
}
