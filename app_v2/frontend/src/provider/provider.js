import providerBase from './base';
import {tokenAuth} from './middlewares';

import {apiUrl} from '../constants/apiUrl';
import {adminOnly} from './helpers';

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
        const {name, token, roles} = this.provider.login(userName, password);
        this.setUserData({name, token, roles});
    }

    setUserData({name, token, roles}) {
        // TODO: need to think about more suitable middleware injection.
        this.user = {name, token, roles};

        this.provider.setMiddlewares([
            tokenAuth(token)
        ]);
    }

    @adminOnly
    async getLines(options = {}) {
        return this.provider.post(
            apiUrl.GET_LINES(),
            options,
        );
    }
}

export const smartSystemApi = new SmartSystemApi();
