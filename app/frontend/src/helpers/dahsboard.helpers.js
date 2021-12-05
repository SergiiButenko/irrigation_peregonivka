import { localizeTime } from "./common.helper";

export const formWeatherData = (data) => {
	let hourlyArr =  data.reduce((acc, hourlyData) => {
            const date = new Date(hourlyData['dt']*1000);
            const time = date.toLocaleTimeString("en-GB", {
                hour: "2-digit",
                minute: "2-digit",
              });
            acc.push({
                'time': time,
                'temp': hourlyData['temp'],
                'humidity': hourlyData['humidity'],
                'weather': hourlyData.weather[0].description,
            })

            return acc;
        }, []);

    hourlyArr.splice(15);

    return hourlyArr
};

export const formIrrigationData = (data) => {
    return data.reduce((acc, el) => {
        const newDate = localizeTime(el['execution_time'])

        const time = newDate.toLocaleTimeString("uk-UA", {
            weekday: "long",
            hour: "2-digit",
            minute: "2-digit",
          });
        

        el.execution_time = time;
        acc.push(el);

        return acc;
    }, []);

}