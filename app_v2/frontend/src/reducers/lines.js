import {handleActions} from 'redux-actions';

const defaultState = {
    loading: true,
    lineFetchError: null,
};

export default handleActions({

    LINES: {
        FAILURE: (state, action) => {
            return {
                ...state,
                lineFetchError: action.payload.message,
            };
        },
        LOADING: (state, action) => {
            return {
                ...state,
                loading: action.payload,
            };
        },
    }
}, defaultState);