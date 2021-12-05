import { localizeTime } from "./common.helper";

export const formSensorData = (data) => {
    return data.reduce((acc, el) => {
        el.date = localizeTime(el.date);
        acc.push(el);

        return acc;
    }, []);

}