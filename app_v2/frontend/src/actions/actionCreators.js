import {createAction} from 'redux-actions';

export function set_active(line_id) {
  return {
    type: 'UPDATE_CARD',
    payload: {line_id, 1}
  }
}

export function set_inactive(line_id) {
  return {
    type: 'UPDATE_CARD',
    payload: {line_id, 0}
  }
}