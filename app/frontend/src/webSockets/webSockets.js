import { io } from "socket.io-client";
import {ACTION_TYPES} from '../constants/websocket';

const socket = io();

export const websocketInit = (store) => {
    socket.on(ACTION_TYPES.error, (payload) => {
        console.log('Error');
        console.log(payload);
    });

    socket.on(ACTION_TYPES.open, (payload) => {
        console.log('Connected to webSocket');
    });

    socket.on(ACTION_TYPES.device_update, (payload) => {
        let path = [''];
        store.dispatch(entity.devices.updateIn(path, payload));
    });

    socket.on(ACTION_TYPES.message, (payload) => {
        let path = [''];
        store.dispatch(entity.devices.updateIn(path, payload));
    });
};

export const emit = ( type, payload ) => socket.emit( type, payload );