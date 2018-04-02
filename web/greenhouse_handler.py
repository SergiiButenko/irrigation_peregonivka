#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import json
import requests
import time
import logging
from helpers import sqlite_database as database
from helpers.redis import *
from helpers.common import *
from controllers import remote_controller as remote_controller


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


SENSORS = {}


def setup_sensors_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        logging.info(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            SENSORS[key] = {'id': row[0],
                            'type': row[1],
                            'base_url': row[2]}

        logging.info(SENSORS)
    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all sensors. {0}".format(e))


def branch_on(line_id, alert_time=7 * 24 * 60):
    """Blablbal."""
    try:
        for attempt in range(2):
            try:
                response = requests.get(url=BACKEND_IP + '/activate_branch', params={"id": line_id, 'time_min': alert_time, 'mode': 'auto'}, timeout=(10, 10))
                response.raise_for_status()
                logging.debug('response {0}'.format(response.text))

                resp = json.loads(response.text)['branches']
                if (resp[str(line_id)]['status'] != 1):
                    logging.error('Branch {0} cant be turned on by rule. response {1}'.format(line_id, response.text))
                    time.sleep(2)
                    continue
                else:
                    logging.info('Branch {0} is turned on by rule'.format(line_id))
                    return response

            except Exception as e:
                logging.error(e)
                logging.error("Can't turn on {0} branch by rule. Exception occured. {1} try out of 2".format(line_id, attempt))
                time.sleep(2)
                continue
        raise Exception("Can't turn on {0} branch".format(line_id))

    except Exception as e:
        logging.error(e)
        logging.error("Can't turn on {0} branch by rule. Exception occured".format(line_id))
        raise Exception("Can't turn on {0} branch".format(line_id))


def branch_off(line_id):
    """Blablbal."""
    try:
        for attempt in range(2):
            try:
                response = requests.get(url=BACKEND_IP + '/deactivate_branch', params={"id": line_id, 'mode': 'auto'}, timeout=(10, 10))
                response.raise_for_status()
                logging.debug('response {0}'.format(response.text))

                resp = json.loads(response.text)['branches']
                if (resp[str(line_id)]['status'] != 0):
                    logging.error('Branch {0} cant be turned off by rule. response {1}. {2} try out of 2'.format(line_id, response.text, attempt))
                    time.sleep(2)
                    continue
                else:
                    logging.info('Branch {0} is turned off by rule'.format(line_id))
                    return response
            except requests.exceptions.Timeout as e:
                logging.error(e)
                logging.error("Can't turn off {0} branch by rule. Timeout Exception occured  {1} try out of 2".format(line_id, attempt))
                time.sleep(2)
                continue
            except Exception as e:
                logging.error(e)
                logging.error("Can't turn off {0} branch by rule. Exception occured. {1} try out of 2".format(line_id, attempt))
                time.sleep(2)
                continue

        raise Exception("Can't turn off {0} branch".format(line_id))

    except Exception as e:
        logging.error(e)
        logging.error("Can't turn off {0} branch by rule. Exception occured".format(line_id))
        raise Exception("Can't turn off {0} branch".format(line_id))


def send_to_viber_bot(rule):
    """Send messages to viber."""
    try:
        id = rule['id']
        rule_id = rule['rule_id']
        line_id = rule['line_id']
        time = rule['time']
        interval_id = rule['interval_id']
        user_friendly_name = rule['user_friendly_name']

        if (rule_id == 2):
            logging.debug("Turn off rule won't be send to viber")
            return

        arr = redis_db.lrange(REDIS_KEY_FOR_VIBER, 0, -1)
        logging.debug("{0} send rule was get from redis".format(arr))
        if (interval_id.encode() in arr):
            logging.debug('interval_id {0} is already send'.format(interval_id))
            return

        try:
            payload = {'rule_id': id, 'line_id': line_id, 'time': time, 'interval_id': interval_id, 'users': USERS, 'timeout': VIBER_SENT_TIMEOUT, 'user_friendly_name': user_friendly_name}
            response = requests.post(VIBER_BOT_IP + '/notify_users_irrigation_started', json=payload, timeout=(10, 10))
            response.raise_for_status()
        except Exception as e:
            logging.error(e)
            logging.error("Can't send rule to viber. Ecxeption occured")
        finally:
            redis_db.rpush(REDIS_KEY_FOR_VIBER, interval_id)
            logging.debug("interval_id: {0} is added to redis".format(interval_id))
            time = 60 * 60 * 60 * 12
            redis_db.expire(REDIS_KEY_FOR_VIBER, time)
            logging.debug("REDIS_KEY_FOR_VIBER: {0} expires in 12 hours".format(REDIS_KEY_FOR_VIBER))
    except Exception as e:
        raise e


def enable_rule():
    while True:
        logging.info("Getting temperature:")
        current_temp = None
        for sensor_id, sensor in SENSORS.items():
            if sensor['type'] == 'air_sensor':
                response = remote_controller.air_sensor(sensor_id)
                current_temp = response[sensor_id]['air_temp']
                logging.info("Air temp: {0}".format(current_temp))
                line_id = response[sensor_id]['id']

        if (current_temp > TEMP_MIN and current_temp < TEMP_MAX):
            logging.info("Current temperature: {0}. Between MIN point: {1} and MAX point: {2}. No action required".format(current_temp, TEMP_MIN, TEMP_MAX))

        if (current_temp >= TEMP_MAX):
            logging.info("Current temperature: {0}. Higher than MAX: {1}. Turn off heating".format(current_temp, TEMP_MAX))
            branch_off(line_id)

        if (current_temp <= TEMP_MIN):
            logging.info("Current temperature: {0}. Lower than MIN: {1}. Turn on heating".format(current_temp, TEMP_MIN))
            branch_on(line_id)
        time.sleep(15 * 60)

if __name__ == "__main__":
    setup_sensors_datalogger()
    enable_rule()
