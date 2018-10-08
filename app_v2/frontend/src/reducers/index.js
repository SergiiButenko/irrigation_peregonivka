import {handleActions} from 'redux-actions';

const defaultState = {lines: {line_id: {id: -1, state: -1}} };

export const test = handleActions({
    UPDATE_CARD: (state, action) => {
        return {
            ...state,
            lines: {
            	...state.lines, 
            	[action.payload.line_id]: 
            		{id:action.payload.line_id,
            		 state:action.payload.state}}
        };
    }
}, defaultState);