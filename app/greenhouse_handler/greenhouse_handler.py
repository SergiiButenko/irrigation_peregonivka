#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import time

import requests

from common import sqlite_database as database
from common.helpers import *
from common.redis_provider import *
from web.controllers import remote_controller as remote_controller


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

requests.packages.urllib3.disable_warnings()

SENSORS = {}
LINES = {}
APP_SETTINGS = {}
TEMP_MIN = None
TEMP_MAX = None
SERVICE_ENABLED = 1
ATTEMPTS = 5


def setup_sensors_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        logging.info(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            SENSORS[key] = {"id": row[0], "type": row[1], "base_url": row[2]}

        logging.info(SENSORS)
    except Exception as e:
        logging.error(
            "Exceprion occured when trying to get settings for all sensors. {0}".format(
                e
            )
        )


def setup_lines_greenlines():
    try:
        lines = database.select(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            LINES[key] = {"id": row[0], "base_url": row[1]}

        logging.info(LINES)
    except Exception as e:
        logging.error(
            "Exceprion occured when trying to get settings for all branches. {0}".format(
                e
            )
        )


def setup_app_settings():
    global APP_SETTINGS, TEMP_MIN, TEMP_MAX, SERVICE_ENABLED
    APP_SETTINGS = database.get_app_settings()

    logging.info("APP settings: {0}".format(APP_SETTINGS))

    SERVICE_ENABLED = int(APP_SETTINGS["greenhouse_auto"]["enabled"])
    if SERVICE_ENABLED == 0:
        logging.info("Service is disabled. Please enable it")
        exit(0)

    TEMP_MAX = int(APP_SETTINGS["temp_min_max"]["max"])
    TEMP_MIN = int(APP_SETTINGS["temp_min_max"]["min"])


def get_line_status(line_id):
    return remote_controller.line_status(line_id=line_id)


def branch_on(line_id, alert_time=7 * 24 * 60):
    """Blablbal."""
    try:
        for attempt in range(ATTEMPTS):
            try:
                response = requests.get(
                    url=BACKEND_IP + "/activate_branch",
                    params={"id": line_id, "time_min": alert_time, "mode": "auto"},
                    timeout=(READ_TIMEOUT, RESP_TIMEOUT),
                    verify=False,
                )
                response.raise_for_status()
                logging.debug("response {0}".format(response.text))

                resp = json.loads(response.text)["branches"]
                if resp[str(line_id)]["status"] != 1:
                    logging.error(
                        "Branch {0} cant be turned on by rule. response {1}".format(
                            line_id, response.text
                        )
                    )
                    time.sleep(2)
                    continue
                else:
                    logging.info("Branch {0} is turned on by rule".format(line_id))
                    return response

            except Exception as e:
                logging.error(e)
                logging.error(
                    "Can't turn on {0} branch by rule. Exception occured. {1} try out of 2".format(
                        line_id, attempt
                    )
                )
                time.sleep(2)
                continue
        raise Exception("Can't turn on {0} branch".format(line_id))

    except Exception as e:
        logging.error(e)
        logging.error(
            "Can't turn on {0} branch by rule. Exception occured".format(line_id)
        )
        raise Exception("Can't turn on {0} branch".format(line_id))


def branch_off(line_id):
    """Blablbal."""
    try:
        for attempt in range(2):
            try:
                response = requests.get(
                    url=BACKEND_IP + "/deactivate_branch",
                    params={"id": line_id, "mode": "manually"},
                    timeout=(READ_TIMEOUT, RESP_TIMEOUT),
                    verify=False,
                )
                response.raise_for_status()
                logging.debug("response {0}".format(response.text))

                resp = json.loads(response.text)["branches"]
                if resp[str(line_id)]["status"] != 0:
                    logging.error(
                        "Branch {0} cant be turned off by rule. response {1}. {2} try out of 2".format(
                            line_id, response.text, attempt
                        )
                    )
                    time.sleep(2)
                    continue
                else:
                    logging.info("Branch {0} is turned off by rule".format(line_id))
                    return response
            except requests.exceptions.Timeout as e:
                logging.error(e)
                logging.error(
                    "Can't turn off {0} branch by rule. Timeout Exception occured  {1} try out of 2".format(
                        line_id, attempt
                    )
                )
                time.sleep(2)
                continue
            except Exception as e:
                logging.error(e)
                logging.error(
                    "Can't turn off {0} branch by rule. Exception occured. {1} try out of 2".format(
                        line_id, attempt
                    )
                )
                time.sleep(2)
                continue

        raise Exception("Can't turn off {0} branch".format(line_id))

    except Exception as e:
        logging.error(e)
        logging.error(
            "Can't turn off {0} branch by rule. Exception occured".format(line_id)
        )
        raise Exception("Can't turn off {0} branch".format(line_id))


def send_to_viber_bot(rule):
    """Send messages to viber."""
    try:
        id = rule["id"]
        rule_id = rule["rule_id"]
        line_id = rule["line_id"]
        time = rule["time"]
        interval_id = rule["interval_id"]
        user_friendly_name = rule["user_friendly_name"]

        if rule_id == 2:
            logging.debug("Turn off rule won't be send to viber")
            return

        arr = redis_db.lrange(REDIS_KEY_FOR_VIBER, 0, -1)
        logging.debug("{0} send rule was get from redis".format(arr))
        if interval_id.encode() in arr:
            logging.debug("interval_id {0} is already send".format(interval_id))
            return

        try:
            payload = {
                "rule_id": id,
                "line_id": line_id,
                "time": time,
                "interval_id": interval_id,
                "users": USERS,
                "timeout": VIBER_SENT_TIMEOUT,
                "user_friendly_name": user_friendly_name,
            }
            response = requests.post(
                VIBER_BOT_IP + "/notify_users_irrigation_started",
                json=payload,
                timeout=(READ_TIMEOUT, RESP_TIMEOUT),
                verify=False,
            )
            response.raise_for_status()
        except Exception as e:
            logging.error(e)
            logging.error("Can't send rule to viber. Ecxeption occured")
        finally:
            redis_db.rpush(REDIS_KEY_FOR_VIBER, interval_id)
            logging.debug("interval_id: {0} is added to redis".format(interval_id))
            time = 60 * 60 * 60 * 12
            redis_db.expire(REDIS_KEY_FOR_VIBER, time)
            logging.debug(
                "REDIS_KEY_FOR_VIBER: {0} expires in 12 hours".format(
                    REDIS_KEY_FOR_VIBER
                )
            )
    except Exception as e:
        raise e


def enable_rule():
    logging.info("Getting temperature:")
    current_temp = None

    for sensor_id, sensor in SENSORS.items():
        if sensor["type"] == "air_sensor":
            response = remote_controller.air_sensor(sensor_id)
            current_temp = response[sensor_id]["air_temp"]
            logging.info("Air temp: {0}".format(current_temp))

    if current_temp > TEMP_MIN and current_temp < TEMP_MAX:
        logging.info(
            "Current temperature: {0}. Between MIN point: {1} and MAX point: {2}. No action required".format(
                current_temp, TEMP_MIN, TEMP_MAX
            )
        )

    if current_temp >= TEMP_MAX:
        logging.info(
            "Current temperature: {0}. Higher than MAX: {1}. Turn off heating".format(
                current_temp, TEMP_MAX
            )
        )
        state = get_line_status(line_id=HEAT_ID)
        if state[HEAT_ID]["state"] != 0:
            branch_off(HEAT_ID)
        else:
            logging.info("Current state: {0}. No action performed".format(state))

    if current_temp <= TEMP_MIN:
        logging.info(
            "Current temperature: {0}. Lower than MIN: {1}. Turn on heating".format(
                current_temp, TEMP_MIN
            )
        )
        state = get_line_status(line_id=HEAT_ID)
        if state[HEAT_ID]["state"] != 1:
            branch_on(HEAT_ID)
        else:
            logging.info("Current state: {0}. No action performed".format(state))


if __name__ == "__main__":
    remote_controller.init_remote_lines()
    setup_sensors_datalogger()
    setup_lines_greenlines()
    setup_app_settings()
    enable_rule()
