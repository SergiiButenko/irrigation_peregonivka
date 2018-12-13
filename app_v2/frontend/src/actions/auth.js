import {createActions} from 'redux-actions';

import {smartSystemApi} from '../provider';

const actions = {
    AUTH: {
        START: v => v,
        SUCCESS: v => v,
        FAILURE: v => v,
        LOGOUT: v => v,
    }
};

const {auth} = createActions(actions);

export function loginByAccessToken() {

    return async dispatch => {
        const apiKey = localStorage.getItem('login');
        if (!apiKey)
            return;

        dispatch(auth.start());
        try {

            await smartSystemApi.login(apiKey);

            const user = smartSystemApi.user;

            const {name, apiKey} = user.attributes;
            if (!name) {
                throw Error('Invalid user; name attribute must be present');
            }
            smartSystemApi.setUserData({apiKey: apiKey});

            dispatch(auth.success({apiKey, user}));

        } catch (e) {

            dispatch(auth.failure(e));
        }
    };

}

export function login(username, password) {

    return async dispatch => {
        dispatch(auth.start());
        try {
            await smartSystemApi.login(username, password);

            const user = smartSystemApi.provider.user;

            const {name, apiKey} = user.attributes;
            if (!name) {
                throw Error('Invalid user; name attribute must be present');
            }

            smartSystemApi.setUserData({apiKey: apiKey});

            localStorage.setItem('login', apiKey);

            dispatch(auth.success({apiKey, user}));

        } catch (e) {
            dispatch(auth.failure(e));
        }
    };
}


export function logout() {
    localStorage.setItem('login', '');
    return dispatch => {
        dispatch(auth.logout());
    };
}
