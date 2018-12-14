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
        const token = localStorage.getItem('login');
        if (!token)
            return;

        dispatch(auth.start());
        try {

            await smartSystemApi.login(token);

            const user = smartSystemApi.user;

            const {name, token, roles} = user.attributes;
            if (!name) {
                throw Error('Invalid user; name attribute must be present');
            }

            smartSystemApi.setUserData({name, token, roles});

            localStorage.setItem('login', token);

            dispatch(auth.success({name, token, roles}));

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

            const user = smartSystemApi.user;

            const {name, token, roles} = user.attributes;
            if (!name) {
                throw Error('Invalid user; name attribute must be present');
            }

            smartSystemApi.setUserData({name, token, roles});

            localStorage.setItem('login', token);

            dispatch(auth.success({name, token, roles}));

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
