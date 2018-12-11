import {createSelector} from 'reselect';
import {LINE_TYPE} from '../constants/lines';

const getAllLines = (state) => state.lines;

export const getIrrigationLines = createSelector(
    [getAllLines],
    (lines) => {
        let arr = [];
        for (let id in lines) {
            if (lines[id].type === LINE_TYPE.IRRIGATION) {
                arr.push(lines[id]);
            }
        }

        return {
            lines: arr,
            loading: lines.loading,
        };
    }
);