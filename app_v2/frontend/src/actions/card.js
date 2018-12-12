import {createAction, createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';

const actionLinesSet = createAction('LINES/SET');

const actions = {
    LINES: {
        LOADING: v => v,
        FAILURE: v => v,
    }
};

const {lines} = createActions(actions);

export const fetchLines = (type) => {
    return async dispatch => {
        dispatch(lines.loading(true));

        try {
            const linesForCard = await smartSystemApi.getLines(type);
            dispatch(actionLinesSet(linesForCard));
        } catch (e) {
            dispatch(lines.failure(e));
        }
        dispatch(lines.loading(false));
    };
};