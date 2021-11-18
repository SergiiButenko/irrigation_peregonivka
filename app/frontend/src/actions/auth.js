import { createActions } from 'redux-actions';

import { smartSystemApi } from '../provider';
import { getTokensIntoLocalStorage, isTokenExpired, setTokensIntoLocalStorage } from '../helpers/auth.helper';

const actions = {
    AUTH: {
        START: v => v,
        SUCCESS: v => v,
        FAILURE: v => v,
        LOGOUT: v => v,
        REFRESH: v => v,
    }
};

const { auth } = createActions(actions);


export const login = (username, password) => {
    return async dispatch => {
        dispatch(auth.start());
        try {
            await smartSystemApi.login(username, password);

            setTokensIntoLocalStorage(smartSystemApi.user);

            dispatch(auth.success(smartSystemApi.user));
        } catch (e) {
            dispatch(auth.failure(e));
        }
    };
};

export const logout = () => {
    return async dispatch => {
        await smartSystemApi.logout();
        
        setTokensIntoLocalStorage({ accessToken: '', refreshToken: '' });

        dispatch(auth.logout());
    };
};

export const validateAccessToken = () => {
    return async dispatch => {
        const accessToken = getTokensIntoLocalStorage().accessToken

        if (!accessToken && isTokenExpired(parseJwt(accessToken))) {
            return;
        }

        try {
            dispatch(auth.start());
        
            await smartSystemApi.setUserByAccessToken(accessToken);
        
            setTokensIntoLocalStorage(smartSystemApi.user);
        
            dispatch(auth.success(smartSystemApi.user));
        } catch (e) {
            dispatch(auth.failure(e));
            return;
        }
    };
};