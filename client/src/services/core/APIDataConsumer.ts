import axios from 'axios';

class APIDataConsumer {
  host;

  constructor() {
    this.host = 'http://localhost:8000';
  }

  makePostRequest(params: unknown, endpoint: string) {
    return axios.post(`${this.host}/${endpoint}`, params);
  }

  makeGetRequest(endpoint: string) {
    return axios.get(`${this.host}/${endpoint}`);
  }
}

export default new APIDataConsumer();
