import {handleActions} from 'redux-actions';

const defaultState = {lines: {}};

export const test = handleActions({
    UPDATE_CARD: (state, action) => {
        return {
            ...state,
            lines: {
                ...state.lines, 
                [action.payload.id]: 
                    {id:action.payload.id,
                        state:action.payload.state}}
        };
    },
    ADD_CARD: (state, action) => {
        return {
            ...state,
            lines: {
                ...state.lines, 
                [action.payload.id]: 
                    {id:action.payload.id,
                        state:action.payload.state}}
        };
    },
    DELETE_CARD: (state, action) => {
        return {
            ...state,
            lines: {
                ...state.lines, 
                [action.payload.id]:[...state.lines[action.payload.id]]
                    .filter((id) => id !== action.payload.id)}
        };
    }
}, defaultState);