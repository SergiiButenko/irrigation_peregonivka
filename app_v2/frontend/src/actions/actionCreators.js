import {createAction} from 'redux-actions';

export function set_state(line_id, state) {
  return {
    type: 'UPDATE_CARD',
    payload: {id: line_id, state: state == true ? 1 : 0}
  }
}