import { ACTION_TYPES } from '../constants/websocket';
import { entity, devices } from '../actions/device';
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
        const event = JSON.parse(income_event.data);

        switch (event.action) {
            case ACTION_TYPES.component_update:
                const component = event.payload.component;
                const state = {
                    'expected_state': event.payload.expected_state,
                    'interval': event.payload.interval
                };
                console.log("updating from sockets")
                console.log(state)
                store.dispatch(devices.loading(true));
                store.dispatch(entity.devices.updateIn(
                    [
                        'components',
                        component.id,
                        'state'
                    ], state
                ));
                store.dispatch(devices.loading(false));
                break;
            default:
                break;
        }

    };
};

export const emit = (type, payload) => socket.emit(type, payload);