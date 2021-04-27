#!/usr/bin/python3
# -*- coding: utf-8 -*-
import functools
import logging
import time
from datetime import datetime

import requests

from notificator import config
from backend import remote_controller
import redis_provider

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


def should_be_notified(key, timeout):
    last_time_sent = redis_provider.get_time_last_notification(key=key)
    
    if last_time_sent is None:
        redis_provider.set_time_last_notification(key=key, date=datetime.now())
        return True
        
    delta = datetime.now() - last_time_sent
    if delta.seconds > 60 * timeout:
        return True

    return False

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

    air_sensor = [line for line in LINES.items() if line['line_type'] == "air_sensor"]
    if len(air_sensor) == 0:
        raise ValueError("No air_sensor found")
    elif len(air_sensor) >= 2:
        raise ValueError("More than 2 air sensors")

    line_id = air_sensor[0]['branch_id']
    response = remote_controller.air_sensor(line_id)
    current_temp = response[line_id]["air_temp"]
    logging.info("Air temp: {0}".format(current_temp))

    TEMP_MAX = APP_SETTINGS["temp_min_max"]["max_alert"]
    TEMP_MIN = APP_SETTINGS["temp_min_max"]["min_alert"]
    if current_temp >= TEMP_MAX:
        logging.warn(
            f"Current temperature: {current_temp}. above MAX point: {TEMP_MAX}. Sending message"
            )
        key = "max_alert"
        message = f"Зверніть увагу. Температура в теплиці {current_temp} градусів"
        timeout = config.TIMEOUT_GRENHOUSE_TEMP_MAX
        try_notify(message, key, timeout)
    elif current_temp <= TEMP_MIN:
        logging.warn(
            f"Current temperature: {current_temp}. below MIN point: {TEMP_MIN}. Sending message"
        )
        key = "max_alert"
        message = f"Зверніть увагу. Температура в теплиці {current_temp} градусів"
        timeout = config.TIMEOUT_GRENHOUSE_TEMP_MIN
        try_notify(message, key, timeout)
    else:
        logging.info(
            f"Current temperature: {current_temp}. Between MIN point: {TEMP_MIN} and MAX point: {TEMP_MAX}. No action required"
        )


if __name__ == '__main__':
    while 1:
        check_conditions()
        logging.info("Sleeping for {} minutes".format(config.RESTART_INTERVAL_MIN / 60))
        time.sleep(config.RESTART_INTERVAL_MIN)