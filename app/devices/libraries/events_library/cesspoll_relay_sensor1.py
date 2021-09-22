from datetime import datetime, timedelta
from devices.service_providers.telegram_bot import telegram_bot
from devices.messages.TelegramMessages import TelegramMessages


class CesspollRelaySensor1:
    class WaterLevel:
        async def analyse(device, sensors_id, deviceCMD, DeviceSQL, sensor_qrs, logger):
            telegram_user = await DeviceSQL.get_linked_telegram_user(
                device.device_id, sensors_id
            )

            sorting = [("date", "DESC")]
            minutes_from_now = 60
            filter = {
                "date": {"$gte": datetime.now() - timedelta(minutes=minutes_from_now)}
            }

            data = await sensor_qrs.get_sensor_values_by_id(
                device.device_id, sensors_id, filter, sorting
            )

            if data is None:
                logger.warn(
                    "No data to work with. Possibly sensors is out of duty. Please check"
                )
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.SENSOR_OUT_OF_SERVICE.format(device.device_id),
                )
                return

            if len(data) == 1:
                logger.warn(
                    "Too few data to analyze"
                )
                return

            curr_level = data[0].data["level"]
            prev_level = data[1].data["level"]
            if curr_level > prev_level:
                logger.info("Cesspoll has became full. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.WATER_LEVEL_BECAME_FULL,
                )
            elif curr_level < prev_level:
                logger.info("Cesspoll has became empty. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.WATER_LEVEL_BECAME_EMPTY,
                )
            elif curr_level == 1 and curr_level == prev_level:
                logger.info("Cesspoll is still full. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.WATER_LEVEL_FULL,
                )
            elif curr_level == 0 and curr_level == prev_level:
                logger.info("Cesspoll is empty. doing nothing")
            else:
                logger.warn(
                    "Cesspoll water level is in unpredicted state. Please check"
                )

    class PumpStarter:
        async def analyse(device, sensors_id, deviceCMD, DeviceSQL, sensor_qrs, logger):
            telegram_user = await DeviceSQL.get_linked_telegram_user(
                device.device_id, sensors_id
            )

            sorting = [("date", "DESC")]
            minutes_from_now = 60
            filter = {
                "date": {"$gte": datetime.now() - timedelta(minutes=minutes_from_now)}
            }

            data = await sensor_qrs.get_sensor_values_by_id(
                device.device_id, sensors_id, filter, sorting
            )

            if data is None:
                logger.warn(
                    "No data to work with. Possibly sensors is out of duty. Please check"
                )
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.SENSOR_OUT_OF_SERVICE.format(device.device_id),
                )
                return

            if len(data) == 1:
                logger.warn(
                    "Too few data to analyze"
                )
                return

            curr_level = data[0].data["level"]
            prev_level = data[1].data["level"]
            if curr_level > prev_level:
                logger.info("Cesspoll pump has beed turned on. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.CESSPOLL_PUMP_TURNED_ON,
                )
            elif curr_level < prev_level:
                logger.info("Cesspoll pump has beed turned off. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.CESSPOLL_PUMP_TURNED_OFF,
                )
            elif curr_level == 1 and curr_level == prev_level:
                logger.info("Cesspoll pump is still on. sending notifications")
                telegram_bot.send_message(
                    telegram_user.id,
                    TelegramMessages.CESSPOLL_PUMP_ON,
                )
            elif curr_level == 0 and curr_level == prev_level:
                logger.info("Cesspoll pump is off. doing nothing")
            else:
                logger.warn("Cesspoll is in unpredicted state. Please check")