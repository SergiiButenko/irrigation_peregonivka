import {createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';
import {arrayToObj} from "../helpers/common.helper";
import {filterSelectedComponents, prepareComponentsTaskObject} from '../helpers/groups.helper';

const actions = createActions(
    {
        ENTITY:{
            GROUPS: {
                UPDATE_IN: (path, value) => ( {path, value} ),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }    
        },
        GROUPS: {
            LOADING: v => v,
            FAILURE: v => v,
        }    
    }
);

export const {groups, entity} = actions;

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

export const fetchGroupComponentsById = (groupId) => {
    return async dispatch => {
        dispatch(groups.loading(true));

        try {
            let groups_input = arrayToObj(await smartSystemApi.getGroup());
            dispatch(entity.groups.updateBatch(groups_input));

            let components = await smartSystemApi.getGroupComponentsById(groupId);
            components = arrayToObj(components)
            dispatch(entity.groups.updateIn([groupId, 'components'], components));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
        dispatch(groups.loading(false));
    };
};


export const toggleSelection = (groupId, componentId, time, quantity) => {
    return async (dispatch, getState) => {
        try {
            const groups = getState().entity.groups.toJS();
            const isSelected = !!groups[groupId].components[componentId].selected;

            dispatch(entity.groups.updateIn([groupId, 'components', componentId, 'selected'], !isSelected));
            if (isSelected) {
                //Remove time in case user deleselect card
                dispatch(entity.groups.updateIn(
                    [groupId, 'components', componentId, 'selectedSettings'],
                    null));
            } else {
                // Set time in case user select card
                dispatch(entity.groups.updateIn(
                    [groupId, 'components', componentId, 'selectedSettings'],
                    {time, quantity}));
            }
            
        }
        catch (e) {
            console.log(e);
        }
    };
};

export const setSelected = (groupId, componentId, time, quantity) => {
    return async (dispatch) => {
        try {
            dispatch(
                entity.groups.updateIn(
                    [groupId, 'components', componentId, 'selected'], true
                )
            );
        
            dispatch(
                entity.groups.updateIn(
                    [groupId, 'components', componentId, 'selectedSettings'],
                    {time, quantity}
                )
            );
            
        }
        catch (e) {
            console.log(e);
        }
    };
};


export const postDeviceTasks = (groupId, minutes) => {
    return async (dispatch, getState) => {
        dispatch(groups.loading(true));

        try {
            const groups = getState().entity.groups.toJS();
            const group = groups[groupId]

            const dataToSend = prepareComponentsTaskObject(group, minutes);
            // console.log(dataToSend);
            await smartSystemApi.postDeviceTasks(dataToSend);
        }
        catch (e) {
            console.log(e);
        }
        
        dispatch(groups.loading(false));
    };
};
