import {combineReducers} from 'redux';

import devices from './devices';
import groups from './groups';
import dashboard from './dashboard';

export default combineReducers({
    devices,
    groups,
    dashboard
});





