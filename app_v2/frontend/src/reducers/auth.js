import {handleActions} from 'redux-actions';

const defaultState = {
    user: null,
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
                user: null,
                loginError: action.payload,
            };
        },
        SUCCESS: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                user: action.payload.user,
                loginError: null,
            };
        },
        LOGOUT: (state) => {
            return {
                ...state,
                loggingIn: false,
                user: null,
            };
        }
    }
}, defaultState);