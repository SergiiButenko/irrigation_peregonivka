import providerBase from './base';
import {apiKeyAuth} from './middlewares';

import {apiUrl} from '../constants/apiUrl';

class SmartSystemApi {
    config = {};

    constructor(config = {}) {
        this.provider = providerBase;
        this.setGlobalConfig(config);
        this.user = {};
    }

    setGlobalConfig(config) {
        this.config = config;
        this.provider.setGlobalConfig(config);
    }

    login(userName, password) {
        const {name, apiKey} = this.provider.login(userName, password);
        this.setUserData({name, apiKey});
    }

    setUserData({name, apiKey}) {
        // TODO: need to think about more suitable middleware injection.
        this.user = {name, apiKey}

        this.provider.setMiddlewares([
            apiKeyAuth(apiKey)
        ]);
    }

    async getLines(options = {}) {
        return this.provider.post(
            apiUrl.GET_LINES(),
            options,
        );
    }
}

export const smartSystemApi = new SmartSystemApi();
