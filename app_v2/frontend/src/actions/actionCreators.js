import {createAction} from 'redux-actions';

export function set_state(line_id, state) {
  return {
    type: 'UPDATE_CARD',
    payload: {id: line_id, state: state == true ? 1 : 0}
  }
}

export function add_card(line_id) {
  return {
    type: 'ADD_CARD',
    payload: {id: line_id, state: 0}
  }
}

export function remove_card(line_id) {
  return {
    type: 'DELETE_CARD',
    payload: {id: line_id}
  }
}