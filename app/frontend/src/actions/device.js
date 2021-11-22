import {createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';
import {arrayToObj} from '../helpers/common.helper';

const actions = createActions(
    {
        ENTITY:{
            DEVICES: {
                UPDATE_IN: (path, value) => ( {path, value} ),
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

export const {devices, entity} = actions;

const deviceKey = 'devices';
const actuatorKey = 'actuator';
const stateKey = 'state';
const selectedKey = 'selected';
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
                    deviceId,
                    actuatorKey,
                    actuatorId
                ], component));

            const state = await smartSystemApi.getDeviceComponentState(componentId);
            dispatch(entity.devices.updateIn(
                [
                    deviceId,
                    actuatorKey,
                    actuatorId,
                    stateKey
                ], state));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
    
}
