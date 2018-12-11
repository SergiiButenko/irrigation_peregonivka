import {handleActions} from 'redux-actions';

const defaultState = {
    lines: {},
    loading: true,
    lineFetchError: null,
};

export default handleActions({

    LINES: {
        ADD_BATCH: (state, action) => {
            return {
                ...state,
                lines: action.payload,
                loginError: null,
            };
        },
        FAILURE: (state, action) => {
            return {
                ...state,
                lineFetchError: action.payload,
            };
        },
        LOADING: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                loading: action.payload,
            };
        },
        LOGOUT: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                accessToken: null,
                user: null,
                mfaRequired: false,
                test: action.payload
            };
        }
    }
}, defaultState);