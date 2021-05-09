import functools
import logging
import time
from datetime import datetime

import redis_provider
import requests
import sqlite_database as database
from backend.remote_controller import (air_sensor, ground_sensor, line_status,
                                       setup_lines_remote_control)
from sensor_data_collector import config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        LOGGER.info('Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        LOGGER.info('Job "%s" completed' % func.__name__)
        return result
    return wrapper


def try_notify(message, key, timeout):
    if should_be_notified(key, timeout) is False:
        logging.info("Timeout is not reached")
        return

    message = {
        "users": config.USERS,
        "message": message
    }

    LOGGER.info(f"Sending '{message}' to messenger")
    r = requests.post(
        config.WEBHOOK_URL_BASE + "/message",
        json=message,
        verify=False,
    )
    r.raise_for_status()

    redis_provider.set_time_last_notification(key=key, date=datetime.now())


def should_be_notified(key, timeout):
    last_time_sent = redis_provider.get_time_last_notification(key=key)

    if last_time_sent is None:
        logging.warn(f"No {key} exists in redis. Allowed")
        return True

    delta = datetime.now() - last_time_sent
    if delta.seconds > 60 * timeout:
        logging.info(f"Seconds passed {delta.seconds} . Allowed")
        return True

    logging.info(f"Seconds not passed {delta.seconds}. Rejected")
    return False


def get_sensor(lines, sensor_type):
    sensor = [line for line in lines.values() if line['line_type']
              == sensor_type]
    if len(sensor) == 0:
        raise ValueError(f"No {sensor_type} found")
    elif len(sensor) >= 2:
        raise ValueError(f"More than 2 {sensor_type} sensors")

    return sensor


@with_logging
def check_conditions():
    r = requests.get(
        url=config.BACKEND_IP,
        verify=False,
    )
    r.raise_for_status()

    LINES = r.json()['line_settings']
    LOGGER.info(str(LINES))

    r = requests.get(
        url=config.BACKEND_IP + '/app_settings',
        verify=False,
    )
    r.raise_for_status()

    APP_SETTINGS = r.json()['data']
    LOGGER.info(str(APP_SETTINGS))
    TEMP_MAX = float(APP_SETTINGS["temp_min_max"]["max_alert"])
    TEMP_DELTA = float(APP_SETTINGS["temp_min_max"]["delta_alert"])
    _now = datetime.now()

    inner_air_sensor = get_sensor(LINES, "air_sensor")
    outer_air_sensor = get_sensor(LINES, "ground_sensor")

    line_id = inner_air_sensor[0]['branch_id']
    response = air_sensor(line_id)
    _q = "INSERT into temperature (line_id, temp, hum, datetime) values ({0}, '{1}', '{2}', '{3}')"
    database.update(
        _q.format(
            response[line_id]["id"],
            response[line_id]["air_temp"],
            response[line_id]["air_hum"],
            _now.strftime("%Y-%m-%d %H:%M"),
        )
    )

    inner_current_temp = float(response[line_id]["air_temp"])
    logging.info(f"Inner Air temp: {inner_current_temp}")

    line_id = outer_air_sensor[0]['branch_id']
    response = ground_sensor(line_id)
    _q = "INSERT into temperature (line_id, temp, datetime) values ({0}, '{1}', '{2}')"
    database.update(
        _q.format(
            response[line_id]["id"],
            response[line_id]["ground_temp"],
            _now.strftime("%Y-%m-%d %H:%M"),
        )
    )
    outer_current_temp = float(response[line_id]["ground_temp"])
    logging.info(f"Outer Air temp: {outer_current_temp}")

    _line_status = line_status(line_id=config.HEAT_ID)
    heat_on = int(_line_status[config.HEAT_ID]["state"]) == 1
    logging.info(f"Is heat on: {heat_on}")

    if inner_current_temp >= TEMP_MAX:
        logging.warn(
            f"Current temperature: {inner_current_temp}. above MAX point: {TEMP_MAX}. Sending message"
        )
        key = "max_alert"
        message = f"Зверніть увагу. Температура в теплиці {inner_current_temp} градусів"
        timeout = config.TIMEOUT_GRENHOUSE
        try_notify(message, key, timeout)

    _temp_delta = round(inner_current_temp - outer_current_temp)
    if heat_on is True and _temp_delta <= TEMP_DELTA:
        logging.warn(
            f"Current delta: {_temp_delta}. below TEMP_DELTA point: {TEMP_DELTA}. Sending message"
        )
        key = "delta_alert"
        message = f"Зверніть увагу. Підігрів увімкнено, проте різниця температур повітря та теплиці {_temp_delta} градусів"
        timeout = config.TIMEOUT_GRENHOUSE
        try_notify(message, key, timeout)

    if inner_current_temp <= outer_current_temp:
        logging.warn(
            f"inner_current_temp:{inner_current_temp} < outer_current_temp:{outer_current_temp}. Sending message"
        )
        key = "below_outer_alert"
        message = f"Зверніть увагу. Температура повітря в теплиці({inner_current_temp}) нижча температури повітря({outer_current_temp}). "
        timeout = config.TIMEOUT_GRENHOUSE
        try_notify(message, key, timeout)


if __name__ == "__main__":
    while 1:
        setup_lines_remote_control()
        check_conditions()
        logging.info("Sleeping for {} minutes".format(
            config.RESTART_INTERVAL_SEC / 60))
        time.sleep(config.RESTART_INTERVAL_SEC)
