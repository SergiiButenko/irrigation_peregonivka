import { createActions } from 'redux-actions';
import { smartSystemApi } from '../provider';
import { arrayToObj } from "../helpers/common.helper";
import { prepareComponentsTaskObject } from '../helpers/groups.helper';

const actions = createActions(
    {
        ENTITY: {
            GROUPS: {
                UPDATE_IN: (path, value) => ({ path, value }),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }
        },
        GROUPS: {
            LOADING: v => v,
            FAILURE: v => v,
            COMPONENTS_LOADING: v => v,
        }
    }
);

export const { groups, entity } = actions;

export const fetchGroups = () => {
    return async dispatch => {
        dispatch(groups.loading(true));

        try {
            let groups_input = arrayToObj(await smartSystemApi.getGroup());
            dispatch(entity.groups.updateBatch(groups_input));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
        dispatch(groups.loading(false));
    };
};


export const fetchGroupById = (groupId) => {
    return async dispatch => {
        dispatch(groups.loading(true));

        try {
            let groups_input = arrayToObj( [await smartSystemApi.getGroup(groupId)] )
            dispatch(entity.groups.updateIn([groupId], groups_input[groupId]));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
        dispatch(groups.loading(false));
    };
};


export const fetchGroupComponentsById = (groupId) => {
    return async dispatch => {
        try {
            let groups_input = await smartSystemApi.getGroup();
            let components = await smartSystemApi.getGroupComponentsById(groupId);
            groups_input = arrayToObj(groups_input);
            groups_input[groupId].components = arrayToObj(components)

            dispatch(entity.groups.updateIn([groupId], groups_input[groupId]));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
    };
};


export const toggleSelection = (groupId, componentId) => {
    return async (dispatch, getState) => {
        try {
            const groups = getState().entity.groups.toJS();
            const isSelected = !!groups[groupId].components[componentId].selected;

            dispatch(entity.groups.updateIn([groupId, 'components', componentId, 'selected'], !isSelected));
        }
        catch (e) {
            console.log(e);
        }
    };
};

export const setSelected = (groupId, componentId) => {
    return async (dispatch) => {
        try {
            dispatch(
                entity.groups.updateIn(
                    [groupId, 'components', componentId, 'selected'], true
                )
            );
        }
        catch (e) {
            console.log(e);
        }
    };
};

export const changeSettings = (groupId, componentId, key, val) => {
    return async (dispatch, getState) => {
        try {
            const groups = getState().entity.groups.toJS();
            const group = groups[groupId];
            let settings = group.components[componentId].settings;
            settings[key] = val;

            dispatch(
                entity.groups.updateIn(
                    [groupId, 'components', componentId, 'settings'], settings
                )
            );
        }
        catch (e) {
            console.log(e);
        }
    };
};


export const createIntervals = (groupId, minutes) => {
    return async (dispatch, getState) => {
        dispatch(groups.loading(true));

        try {
            const groups = getState().entity.groups.toJS();
            const group = groups[groupId];
            
            const dataToSend = prepareComponentsTaskObject(group, minutes);
            await smartSystemApi.createIntervals(dataToSend);

            Object.keys(group.components).map((componentId, index) => {
                if (group.components[componentId].selected) {
                    dispatch(
                        entity.groups.updateIn(
                            [groupId, 'components', componentId, 'selected'], false
                        )
                    );
                }
            });
        }
        catch (e) {
            console.log(e);
        }

        dispatch(groups.loading(false));
    };
};
