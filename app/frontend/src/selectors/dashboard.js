import {createSelector} from 'reselect';

const getDashboardState = (state) => state.dashboard;
const getDashboardData = (state) => { return state.entity.dashboard ? state.entity.dashboard.toJS() : null };

export const getDashboard = createSelector(
    [getDashboardData, getDashboardState],
    (data, dashboardState) => {        
        return {
            ...dashboardState,
            data: data.data,
        };
    }
);