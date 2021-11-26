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

const deviceKey = 'devices';
const stateKey = 'state';
const tasksKey = 'tasks';

export const fetchDevices = () => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {
            let devices = await smartSystemApi.getDevice();
            // for (let _device in devices[deviceKey]) {
            //     _device.lines = arrayToObj(devices.lines);
            // }

            devices = arrayToObj(devices[deviceKey]);

            dispatch(entity.devices.updateBatch(devices));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const fetchDeviceById = (deviceId) => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {

            const _devices = await smartSystemApi.getDeviceById(deviceId);
            let device = _devices[deviceKey][0];
            // device.lines = arrayToObj(device.lines);

            dispatch(entity.devices.set(device));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};

export const fetchDeviceTasks = (deviceId) => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {

            const _devices = await smartSystemApi.getDeviceLatestTask(deviceId);
            const tasks = _devices[tasksKey];

            for (task in tasks) {
                dispatch(entity.devices.updateIn(
                    [
                        deviceId,
                        linesKey,
                        task.line_id,
                        tasksKey
                    ], task.list));
            }
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
                    stateKey
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const setComponentState = (componentId, state, interval) => {
    return async (dispatch, getState) => {
        dispatch(devices.loading(true));
        try {
            const devices = getState().entity.devices.toJS();
            const component = devices.components[componentId];
            
            let dataToSend = {
                components: [{
                    component_id: component.id,
                    rules: {
                        time: component.settings.minutes,
                        intervals: component.settings.quantity,
                        time_wait: component.settings.minutes * 1.5
                    }
                }],
                minutes_delay: 0
            };
            
            await smartSystemApi.postDeviceTasks(dataToSend);

            const state = await smartSystemApi.getDeviceComponentState(componentId);
            dispatch(entity.devices.updateIn(
                [
                    'components',
                    componentId,
                    stateKey
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};