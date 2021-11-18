import { createActions } from 'redux-actions';
import { smartSystemApi } from '../provider';
import { arrayToObj } from "../helpers/common.helper";

const actions = createActions(
    {
        ENTITY: {
            DASHBOARD: {
                UPDATE_IN: (path, value) => ({ path, value }),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }
        },
        DASHBOARD: {
            LOADING: v => v,
            FAILURE: v => v,
        }
    }
);

export const { dashboard, entity } = actions;

export const fetchDashboard = () => {
    return async dispatch => {
        dispatch(dashboard.loading(true));

        try {
            let data = await smartSystemApi.getDashboard();            
            dispatch(entity.dashboard.updateIn(['data'], data));
        }
        catch (e) {
            dispatch(dashboard.failure(e));
        }

        dispatch(dashboard.loading(false));
    };
};
