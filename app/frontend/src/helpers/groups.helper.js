export const filterSelectedComponents = (components) => {
	return Object.keys(components).reduce((acc, key) => {
            if (components[key].selected) {
                acc[key] = components[key];
            }
            
            return acc;
        }, {});
};


export const prepareComponentsTaskObject = (group, minutes) => {
    const filtered = filterSelectedComponents(group.components);

    let dataToSend = {
        components: null,
        minutes_delay: minutes
    };

    dataToSend.components = Object.keys(filtered).reduce((acc, key) => {
        let component = group.components[key]
        let v = {
            component_id: component.id,
            rules: {
                time: component.settings.minutes,
                intervals: component.settings.quantity,
                time_wait: component.settings.minutes * 1.5
            }
        }   
        acc.push(v);
    
        return acc;
    }, []);

    return dataToSend;
 }