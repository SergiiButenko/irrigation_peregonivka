import { ACTION_TYPES } from '../constants/websocket';
import { entity, devices } from '../actions/device';
import { formSensorData } from '../helpers/components.helper';
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
        const component = event.payload.component;
                
        switch (event.action) {
            case ACTION_TYPES.actuator_update:
                store.dispatch(devices.updating(true));
                
                const state = {
                    'expected_state': event.payload.expected_state,
                    'interval': event.payload.interval
                };
                
                store.dispatch(entity.devices.updateIn(
                    [
                        'components',
                        component.id,
                        'state'
                    ], state
                ));
                
                store.dispatch(devices.updating(false));
                break;

            case ACTION_TYPES.sensor_update:
                component.data = formSensorData(event.payload.data);
                store.dispatch(entity.devices.updateIn(
                    [
                        'components',
                        component.id,
                    ], component
                ));
                
                store.dispatch(devices.updating(false));
                break;

            default:
                break;
        }

    };
};

export const emit = (type, payload) => socket.emit(type, payload);