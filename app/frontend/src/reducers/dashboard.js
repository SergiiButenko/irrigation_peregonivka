import {handleActions} from 'redux-actions';

const defaultState = {
    loading: true,
    dashboardFetchError: null,
};

export default handleActions({
    DASHBOARD: {
        FAILURE: (state, action) => {
            return {
                ...state,
                dashboardFetchError: action.payload,
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