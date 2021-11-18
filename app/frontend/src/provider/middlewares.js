import { logout } from '../actions/auth';
import {parseJwt, isTokenExpired} from '../helpers/auth.helper';
import store from '../store';


export const withAuth = token => (url, opts) => async next => {
    let token = store.getState().auth.user && store.getState().auth.user.accessToken;
    !opts.headers && (opts.headers = {});
    if (!opts.headers.Authorization) {
        opts.headers.Authorization = `Bearer ${token}`;
    }

    return next(url, {
        ...opts,
        headers: {
            ...opts.headers,
        },
    });
};


export const globalErrorHandler = handler => (url, opts) => async next => {
    return next(url, opts).catch(response => handler(response));
};


export const tokenRefresh = (url, opts) => async next => {
    const auth = store.getState().auth

    const accessToken = auth.user && parseJwt(auth.user.accessToken);

    if ( accessToken && isTokenExpired(accessToken) ) {
        logout();
        return;
    }

    return next(url, opts);
};


export const wrapFunctionWithMiddlewares = (func, middlewares) => {
    return  middlewares.reduce((next, fn) =>
        async (...args) => fn(...args)(next), func);
};