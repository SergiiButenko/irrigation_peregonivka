const DEFAULT_POST_OPTIONS = {
    'Content-Type': 'application/json'
};

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
                    .then((response) => {
                        if (response.status >= 200 && response.status < 300) {
                            response.json().then(data => {
                                resolve(reader(data));
                            });
                        } else {
                            reject(response);
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
        options.cache = 'no-cache';
        return this.doRequest(url, options, reader);
    }

    async post(url, body = {}, options = {}, reader = DEFAULT_READER) {
        options = {
            ...options,
            body,
            method: 'POST',
            headers: {
                ...DEFAULT_POST_OPTIONS,
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
                ...DEFAULT_POST_OPTIONS,
                ...options.headers,
            }
        };

        return this.doRequest(url, options, reader);
    }
}
export default new _ProviderBase();