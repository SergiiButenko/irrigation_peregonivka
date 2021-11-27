import { createActions } from 'redux-actions';
import { smartSystemApi } from '../provider';
import { arrayToObj } from '../helpers/common.helper';

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
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                ], component));

            const state = await smartSystemApi.getDeviceComponentState(componentId);
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                    'state'
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const createIntervals = (component) => {
    return async (dispatch) => {
        dispatch(devices.loading(true));
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

            const state = await smartSystemApi.getDeviceComponentState(component.id);
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    component.id,
                    'state'
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};

export const deleteInterval = (componentId, intervalId, expected_state) => {
    return async (dispatch) => {
        dispatch(devices.loading(true));
        
        try {
            await smartSystemApi.deleteInterval(intervalId, {expected_state});

            const state = await smartSystemApi.getDeviceComponentState(componentId);
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                    'state'
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        
        dispatch(devices.loading(false));
    };
};