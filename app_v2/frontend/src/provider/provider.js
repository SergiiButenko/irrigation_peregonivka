import providerBase from './providerBase';

export const URLS = {
    GET_LINES: () => '/api/dx/v1/s3auth',
};




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
