import {createAction} from 'redux-actions';

export function set_state(line_id, state) {
    return {
        type: 'UPDATE_CARD',
        payload: {id: line_id, state: !!state}
    };
}

export function add_card(line_id) {
    return {
        type: 'ADD_CARD',
        payload: {id: line_id, state: 0}
    };
}
