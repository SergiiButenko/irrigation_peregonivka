import {createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';

const actions = {
    LINES: {
        LOADING: v => v,
        FAILURE: v => v,
        UPDATE_IN: (path, value) => ( {path, value} ),
        SET: v => v,
    }
};

const {lines} = createActions(actions);

export const fetchLines = (type) => {
    return async dispatch => {
        dispatch(lines.loading(true));

        try {
            const linesForCard = await smartSystemApi.getLines(type);
            dispatch(lines.set(linesForCard));
        } catch (e) {
            dispatch(lines.failure(e));
        }
        dispatch(lines.loading(false));
    };
};

export default lines;