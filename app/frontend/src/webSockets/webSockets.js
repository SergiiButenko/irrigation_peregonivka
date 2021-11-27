import { io } from "socket.io-client";
import { ACTION_TYPES } from '../constants/websocket';

const socket = io("ws://0.0.0.0");

export const websocketInit = (store) => {
    
    socket.io.on(ACTION_TYPES.error, (payload) => {
        console.log(socket);
        console.log('Error');
        console.log(payload);
    });

    socket.io.on(ACTION_TYPES.connect, (payload) => {
        console.log('Connected to webSocket');
    });

    socket.io.on(ACTION_TYPES.component_update, (payload) => {
        console.log('UPDATE payload');
        console.log(payload);
        // let path = [''];
        // store.dispatch(entity.devices.updateIn(path, payload));
    });
};

export const emit = (type, payload) => socket.emit(type, payload);