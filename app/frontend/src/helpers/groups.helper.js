import { groups } from "../actions/groups";

export const filterSelectedComponents = (components) => {
	return Object.keys(components).reduce((acc, key) => {
            if (components[key].selected && components[key].selected === true) {
                acc[key] = components[key];
            }
            
            return acc;
        }, {});
};


export const prepareComponentsTaskObject = (group, minutes) => {
    const filtered = filterSelectedComponents(group.components);

    let dataToSend = {
        actuators: null,
        minutes_delay: minutes
    };

    dataToSend.actuators = Object.keys(filtered).reduce((acc, key) => {
        let component = group.components[key]
        let v = {
            device_id: component.device_id,
            actuator_id: component.component_id,
            rules: {
                time: component.settings.minutes,
                intervals: component.settings.quantity,
                time_wait: component.settings.minutes * 2
            }
        }   
        acc.push(v);
    
        return acc;
    }, []);

    return dataToSend;
 }