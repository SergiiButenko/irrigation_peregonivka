import {createSelector} from 'reselect';
import {LINE_TYPE} from '../constants/lines';

const getLinesState = (state) => state.lines;
const gitAllLines = (state) => { state.entity.lines ? state.entity.lines.toJS() : null };

export const getIrrigationLines = createSelector(
    [gitAllLines, getLinesState],
    (lines, linesState) => {
        let arr = [];
        for (let id in lines) {
            if (lines[id].type === LINE_TYPE.IRRIGATION) {
                arr.push(lines[id]);
            }
        }

        return {
            ...linesState,
            lines: arr,
        };
    }
);