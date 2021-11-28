// import { io } from "socket.io-client";
import { ACTION_TYPES } from '../constants/websocket';

const ws = new WebSocket('ws://localhost/notification/ws');

export const websocketInit = (store) => {

    ws.onclose = (e) => {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            websocketInit(store);
        }, 1000);
    };

    ws.onerror = (err) => {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
    };

    ws.onmessage = (income_event) => {
        console.log(income_event);
        const event = JSON.parse(income_event.data);

        switch (event.type) {
            case ACTION_TYPES.component_update:
                const component = event.payload;
                console.log(component);
                // store.dispatch(entity.devices.updateIn(path, payload));
                break;
            default:
                break;
        }

    };
};

export const emit = (type, payload) => socket.emit(type, payload);