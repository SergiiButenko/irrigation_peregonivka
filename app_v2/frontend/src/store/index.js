import { createStore, combineReducers, applyMiddleware } from 'redux'

import * as reducers from "../reducers/index";

function logger({ getState }) {
  return next => action => {
    console.log('will dispatch', action)

    // Call the next dispatch method in the middleware chain.
    const returnValue = next(action)

    console.log('state after dispatch', getState())

    // This will likely be the action itself, unless
    // a middleware further in chain changed it.
    return returnValue
  }
}

const combinedReducer = combineReducers({
   ...reducers
});

const store = createStore(
  combinedReducer,
  applyMiddleware(logger)
)

export default store;