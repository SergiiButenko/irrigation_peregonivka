import {combineReducers} from 'redux';

import {lines} from './entity/lines';

const createFilteredReducer = (reducerFunction, reducerPredicate) =>
    (state, action) => {
        const isInitializationCall = state === undefined;
        const shouldRunWrappedReducer = reducerPredicate(action) || isInitializationCall;
        return shouldRunWrappedReducer ? reducerFunction(state, action) : state;
    };

const filter = (key) => action => action.type.startsWith(key);

export default combineReducers({
    line:           createFilteredReducer(lines,          filter('LINES')),
});