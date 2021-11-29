import {handleActions} from 'redux-actions';

const defaultState = {
    loading: true,
    componentsLoading: true,
    groupFetchError: null,
};

export default handleActions({
    GROUPS: {
        FAILURE: (state, action) => {
            return {
                ...state,
                groupFetchError: action.payload,
            };
        },
        LOADING: (state, action) => {
            return {
                ...state,
                loading: action.payload,
            };
        },
        COMPONENTS_LOADING: (state, action) => {
            return {
                ...state,
                componentsLoading: action.payload,
            };
        },

    }
}, defaultState);