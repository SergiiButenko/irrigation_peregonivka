#!/usr/bin/python3
# -*- coding: utf-8 -*-
import functools
import logging
import time

import requests

from scheduler import config
from backend import remote_controller

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


@with_logging
def notify(message):
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

    for line_id, line in LINES.items():
        if line["type"] == "air_sensor":
            response = remote_controller.air_sensor(line_id)
            current_temp = response[line_id]["air_temp"]
            logging.info("Air temp: {0}".format(current_temp))

    TEMP_MAX = APP_SETTINGS["temp_min_max"]["max_alert"]
    TEMP_MIN = APP_SETTINGS["temp_min_max"]["min_alert"]
    if current_temp >= TEMP_MAX:
        logging.warn(
            "Current temperature: {0}. above MAX point: {2}. Sending message".format(
                current_temp, TEMP_MAX
            )
        )
    elif current_temp <= TEMP_MIN:
        logging.warn(
            "Current temperature: {0}. below MIN point: {2}. Sending message".format(
                current_temp, TEMP_MIN
            )
        )
    else:
        logging.info(
            "Current temperature: {0}. Between MIN point: {1} and MAX point: {2}. No action required".format(
                current_temp, TEMP_MIN, TEMP_MAX
            )
        )


if __name__ == '__main__':
    while 1:
        check_conditions()
        logging.info("Sleeping for {} minutes".format(config.RESTART_INTERVAL_MIN / 60))
        time.sleep(config.RESTART_INTERVAL_MIN)