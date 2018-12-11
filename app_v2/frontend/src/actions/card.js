import {createAction, createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';

const actionLinesAddBatch = createAction('LINES/SET');

const actions = {
    LINES: {
        LOADING: v => v,
        ADD_SINGLE: v => v,
        ADD_BATCH: v => v,
        DELETE: v => v,
        FAILURE: v => v,
    }
};

const {lines} = createActions(actions);

export const fetchLines = (type) => {
    return async dispatch => {
        dispatch(lines.loading(true));

        try {
            const linesForCard = await smartSystemApi.getLines(type);
            dispatch(actionLinesAddBatch(linesForCard));
        } catch (e) {
            dispatch(lines.failure(e));
        }
        dispatch(lines.loading(false));
    };
};