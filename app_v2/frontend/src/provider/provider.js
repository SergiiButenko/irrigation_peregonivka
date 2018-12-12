import providerBase from './providerBase';
import {URLS} from '../constants/URLS';

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
            URLS.GET_LINES(),
            options,
        );
    }
}

export const smartSystemApi = new SmartSystemApi();
