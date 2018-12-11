export const apiKeyAuth = apiKey => (url, opts) => async next => {
    return next(url, {
        ...opts,
        headers: {
            ...opts.headers,
            'X-Api-Key': apiKey,
        },
    });
};

export const globalErrorHandler = handler => (url, opts) => async next => {
    return next(url, opts).catch(response => handler(response));
};

export const wrapFunctionWithMiddlewares = (func, middlewares) => {
    return  middlewares.reduce((next, fn) =>
        async (...args) => fn(...args)(next), func);
};