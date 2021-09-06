import axios from 'axios';
class APIDataConsumer {
    host;
    constructor() {
        this.host = 'http://localhost:8000';
    }
    makePostRequest(params, endpoint) {
        return axios.post(`${this.host}/${endpoint}`, params);
    }
    makeGetRequest(endpoint) {
        return axios.get(`${this.host}/${endpoint}`);
    }
}
export default new APIDataConsumer();
//# sourceMappingURL=APIDataConsumer.js.map