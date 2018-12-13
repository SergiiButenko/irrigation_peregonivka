import {handleActions} from 'redux-actions';

const defaultState = {
    user: null,
    accessToken: null,
    loggingIn: false,
    loginError: null,
};

export default handleActions({

    AUTH: {
        START: (state) => {
            return {
                ...state,
                loggingIn: true,
                loginError: null,
            };
        },
        FAILURE: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                accessToken: null,
                user: null,
                loginError: action.payload,
            };
        },
        SUCCESS: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                accessToken: action.payload.accessToken,
                user: action.payload.user,
                loginError: null,
            };
        },
        LOGOUT: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                accessToken: null,
                user: null,
            };
        }
    }
}, defaultState);