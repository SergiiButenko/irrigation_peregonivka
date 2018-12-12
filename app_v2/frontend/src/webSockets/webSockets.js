import io from 'socket.io-client';
import {ACTION_TYPES} from '../constants/websocket';
import lines from '../actions/card';
import config from 'config';

const {endpoints: {ws_uri}} = config;

const socket = io(ws_uri);

export const websocketInit = (store) => {
    socket.on(ACTION_TYPES.error, (payload) => {
        console.log('Error');
        console.log(payload);
    });

    socket.on(ACTION_TYPES.open, (payload) => {
        console.log('Connected to webSocket');
    });

    socket.on(ACTION_TYPES.line_status_update, (payload) => {
        let path = '';
        store.dispatch(lines.updateIn(path, payload));
    });
};

export const emit = ( type, payload ) => socket.emit( type, payload );