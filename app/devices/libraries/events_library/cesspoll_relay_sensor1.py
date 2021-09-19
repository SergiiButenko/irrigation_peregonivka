from datetime import datetime, time, timedelta


class CesspollRelaySensor1:
    class WaterLevel:
        async def analyse(device, sensors_id, deviceCMD, sensor_qrs, logger):
            sorting = [("date", "DESC")]
            minutes_from_now = 60
            filter = {
                "date": {"$gte": datetime.now() - timedelta(minutes=minutes_from_now)}
            }
            
            data = await sensor_qrs.get_sensor_values_by_id(
                device.device_id, sensors_id, filter, sorting
            )
            logger.info(data)

            if data is None:
                logger.warn(
                    "No data to work with. Possibly sensors is out of duty. Please check"
                )

            curr_level = data[0].data["level"]
            prev_level = data[1].data["level"]
            if curr_level > prev_level:
                logger.info("Cesspoll has became full. sending notifications")
            elif curr_level < prev_level:
                logger.info("Cesspoll has became empty. sending notifications")
            elif curr_level == 1 and curr_level == prev_level:
                logger.info("Cesspoll is still full. sending notifications")
            elif curr_level == 0 and curr_level == prev_level:
                logger.info("Cesspoll is empty. doing nothing")
            else:
                logger.warn("Cesspoll water level is in unpredicted state. Please check")
                
    class PumpStarter:
        async def analyse(device, sensors_id, deviceCMD, sensor_qrs, logger):
            sorting = [("date", "DESC")]
            minutes_from_now = 60
            filter = {
                "date": {"$gte": datetime.now() - timedelta(minutes=minutes_from_now)}
            }
            
            data = await sensor_qrs.get_sensor_values_by_id(
                device.device_id, sensors_id, filter, sorting
            )
            logger.info(data)

            if data is None:
                logger.warn(
                    "No data to work with. Possibly sensors is out of duty. Please check"
                )

            curr_level = data[0].data["level"]
            prev_level = data[1].data["level"]
            if curr_level > prev_level:
                logger.info("Cesspoll pump has beed turned on. sending notifications")
            elif curr_level < prev_level:
                logger.info("Cesspoll pump has beed turned off. sending notifications")
            elif curr_level == 1 and curr_level == prev_level:
                logger.info("Cesspoll pump is still on. sending notifications")
            elif curr_level == 0 and curr_level == prev_level:
                logger.info("Cesspoll pump is off. doing nothing")
            else:
                logger.warn("Cesspoll is in unpredicted state. Please check")