import {wrapFunctionWithMiddlewares} from './middlewares';

const DEFAULT_READER = d => d;

class _ProviderBase {

    middlewares = [];
    config = {};

    constructor(config = {}) {
        this.config = config;
    }

    async doRequest(url, options, reader) {
        url = this.prepareURL(url, options);

        const fetchRequest = async (url, options) => {
            return new Promise((resolve, reject) => {
                fetch(url.href, options)
                    .then(async (response) => {
                        try {
                            let resp = reader(await response.json());

                            if (response.status >= 200 && response.status < 300) {
                                resolve(resp);
                            } else {
                                reject(resp);
                            }
                        } catch (error) {
                            console.log("Error");
                            console.log(error);
                            reject(error);
                        }
                    })
                    .catch(reject);
            });
        };

        return wrapFunctionWithMiddlewares(fetchRequest, this.middlewares)(url, options);
    }

    prepareURL(url, { query = {}}) {
        const { base_url } = this.config;

        url = new URL(url, base_url);

        Object.keys(query).forEach(key => url.searchParams.append(key, query[key]));
        return url;
    }

    setGlobalConfig(config = {}) {
        this.config = config;
    }

    setMiddlewares(middlewares) {
        this.middlewares = middlewares;
    }

    async get(url, options = {}, reader = DEFAULT_READER) {
        options.method = 'GET';
        return this.doRequest(url, options, reader);
    }

    async post(url, body = {}, options = {}, reader = DEFAULT_READER) {
        options = {
            ...options,
            body,
            method: 'POST',
            headers: {
                ...options.headers,
            }
        };
        return this.doRequest(url, options, reader);
    }

    async put(url, body = {}, options = {}, reader = DEFAULT_READER) {
        options = {
            ...options,
            body,
            method: 'PUT',
            headers: {
                ...options.headers,
            }
        };

        return this.doRequest(url, options, reader);
    }

    async delete(url, body = {}, options = {}, reader = DEFAULT_READER) {
        options = {
            ...options,
            body,
            method: 'DELETE',
            headers: {
                ...options.headers,
            }
        };

        return this.doRequest(url, options, reader);
    }

}
export default new _ProviderBase();