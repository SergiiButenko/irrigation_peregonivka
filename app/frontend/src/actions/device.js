import { createActions } from 'redux-actions';
import { smartSystemApi } from '../provider';
import { arrayToObj } from '../helpers/common.helper';
import { formSensorData } from '../helpers/components.helper';

const actions = createActions(
    {
        ENTITY: {
            DEVICES: {
                UPDATE_IN: (path, value) => ({ path, value }),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }
        },
        DEVICES: {
            LOADING: v => v,
            FAILURE: v => v,
            UPDATING: v => v,
        }
    }
);

export const { devices, entity } = actions;


export const fetchDevices = () => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {
            let devices = await smartSystemApi.getDevice();
            // for (let _device in devices['devices]) {
            //     _device.lines = arrayToObj(devices.lines);
            // }

            devices = arrayToObj(devices['devices']);

            dispatch(entity.devices.updateBatch(devices));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const initComponent = (componentId) => {
    return async (dispatch) => {
        dispatch(devices.loading(true));
        try {
            const component = await smartSystemApi.getDeviceComponent(componentId);
            const state = await smartSystemApi.getDeviceComponentState(componentId);
            component.state = {
                'expected_state': state.expected_state,
                'interval': state.interval
            };
            
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                ], component));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const initSensor = (componentId) => {
    return async (dispatch) => {
        dispatch(devices.loading(true));
        try {
            const component = await smartSystemApi.getDeviceComponent(componentId);
            const data = await smartSystemApi.getSendorData(componentId);
            component.data = formSensorData(data.data);
            
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                ], component));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const createIntervals = (component) => {
    return async (dispatch) => {
        dispatch(entity.devices.updateIn(
            [
                'components',
                component.id,
                'updating'
            ], true));        
        try {
            const dataToSend = {
                components: [{
                    component_id: component.id,
                    rules: {
                        time: component.settings.minutes,
                        intervals: component.settings.quantity
                    }
                }],
                minutes_delay: 0
            };

            await smartSystemApi.createIntervals(dataToSend);
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
    };
};

export const deleteInterval = (component, intervalId, expected_state) => {
    return async (dispatch) => {
        dispatch(entity.devices.updateIn(
            [
                'components',
                component.id,
                'updating'
            ], true));


        try {
            await smartSystemApi.deleteInterval(intervalId, { expected_state });
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
    };
};