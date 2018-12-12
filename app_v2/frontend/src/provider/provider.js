import providerBase from './base';
import {apiUrl} from '../constants/apiUrl';

class SmartSystemApi {
    config = {};

    constructor(config = {}) {
        this.provider = providerBase;
        this.setGlobalConfig(config);
    }

    setGlobalConfig(config) {
        this.config = config;
        this.provider.setGlobalConfig(config);
    }

    async getLines(options = {}) {
        return this.provider.post(
            apiUrl.GET_LINES(),
            options,
        );
    }
}

export const smartSystemApi = new SmartSystemApi();
