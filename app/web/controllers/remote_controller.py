#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import time
import socket

import requests

from common import sqlite_database as database
from common.common import *
from config.config import *

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

LINES = {}

def get_IP_by_local_domain(url):
    if '.local' in url:
        return socket.gethostbyname(url)
    
    return url

def setup_lines_remote_control():
    """Fill up settings array to save settings for branches."""
    try:
        lines = database.select(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            if row[7] is None and row[9] is None:
                continue

            LINES[key] = {
                "id": row[0],
                "relay_num": row[1],
                "is_pump": row[2],
                "is_except": row[3],
                "group_id": row[4],
                "line_name": row[5],
                "group_name": row[6],
                "base_url": row[7],
                "device_id": row[8],
                "device_url": row[9],
                "pump_enabled": row[10],
                "pump_pin": row[11],
                "state": -1,
            }

        logging.info(LINES)
    except Exception as e:
        logging.error(
            "Exceprion occured when trying to get settings for all branches. {0}".format(
                e
            )
        )


def init_remote_lines():
    setup_lines_remote_control()


def on(line_id):
    """Set pin to high state."""
    try:
        relay = LINES[line_id]["relay_num"]
        base_url = get_IP_by_local_domain(LINES[line_id]["base_url"])
        response_on = requests.get(
            url="http://" + base_url + "/on",
            params={"relay": relay},
            timeout=(READ_TIMEOUT, RESP_TIMEOUT),
        )
        response_on.raise_for_status()

        logging.info("response {0}".format(str(response_on.text)))

        return json.loads(response_on.text)

    except Exception as e:
        logging.error(
            "Exception occured when turning on {0} relay. {1}".format(relay, e)
        )
        raise e


def off(line_id):
    """Set pin to low state."""
    try:
        relay = LINES[line_id]["relay_num"]
        base_url = get_IP_by_local_domain(LINES[line_id]["base_url"])
        response_off = requests.get(
            url="http://" + base_url + "/off",
            params={"relay": relay},
            timeout=(READ_TIMEOUT, RESP_TIMEOUT),
        )
        response_off.raise_for_status()

        logging.info("response {0}".format(str(response_off.text)))

        return json.loads(response_off.text)
    except Exception as e:
        logging.error(
            "Exception occured when turning off {0} relay. {1}".format(relay, e)
        )
        raise e


def air_s(line_id):
    for attempt in range(2):
        try:
            base_url = get_IP_by_local_domain(LINES[line_id]["base_url"])
            response_air = requests.get(
                url="http://" + base_url + "/air_temperature",
                timeout=(READ_TIMEOUT, RESP_TIMEOUT),
            )
            response_air.raise_for_status()

            logging.info("response {0}".format(str(response_air.text)))
            res = json.loads(response_air.text)

            r_dict = {}
            r_dict[line_id] = dict(id=line_id, air_temp=res["temp"], air_hum=res["hum"])

            return r_dict
        except Exception as e:
            logging.error(e)
            time.sleep(2)
            continue
    raise Exception("Can't get temperature. Retries limit reached")


def ground_s(line_id):
    for attempt in range(2):
        try:
            base_url = get_IP_by_local_domain(LINES[line_id]["base_url"])
            response_air = requests.get(
                url="http://" + base_url + "/ground_temperature",
                timeout=(READ_TIMEOUT, RESP_TIMEOUT),
            )
            response_air.raise_for_status()

            logging.info("response {0}".format(str(response_air.text)))
            res = json.loads(response_air.text)

            r_dict = {}
            r_dict[line_id] = dict(id=line_id, ground_temp=res["temp"])

            return r_dict
        except Exception as e:
            logging.error(e)
            time.sleep(2)
            continue
    raise Exception("Can't get temperature. Retries limit reached")


def branch_on(line_id=None, line_alert=None):
    """Turn on branch by id."""
    if line_id is None:
        logging.error("No branch id")
        return None

    if line_alert is None:
        logging.error("No branch alert time")
        return None

    relay = LINES[line_id]["relay_num"]
    status = on(LINES[line_id]["id"])
    r_dict = {}
    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    if LINES[line_id]["pump_enabled"] == 0:
        logging.info("Pump won't be turned on with {0} branch id".format(line_id))
    else:
        time.sleep(5)
        line_id = LINES[line_id]["pump_pin"]
        status = on(line_id=line_id)

        r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))
        
        logging.info("Pump turned on with {0} branch id".format(line_id))

    return r_dict


def branch_off(line_id=None):
    """Turn off branch by id."""
    if line_id is None:
        logging.error("No branch id")
        return None

    relay = LINES[line_id]["relay_num"]
    status = off(LINES[line_id]["id"])
    r_dict = {}
    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    if LINES[line_id]["pump_enabled"] == 1:
        time.sleep(5)
        line_id = LINES[line_id]["pump_pin"]
        status = off(line_id=line_id)
        r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))
        
        logging.info("Pump turned off with {0} branch id".format(line_id))

    return r_dict


def air_sensor(line_id=None):
    if line_id is None:
        logging.error("No line id")
        return None

    return air_s(line_id=line_id)


def ground_sensor(line_id=None):
    if line_id is None:
        logging.error("No line id")
        return None

    return ground_s(line_id=line_id)


def line_status(line_id):
    """Return status of raspberryPi relay."""
    r_dict = {}

    try:
        base_url = get_IP_by_local_domain(LINES[line_id]["base_url"])
        relay = LINES[line_id]["relay_num"]

        response = requests.get(
            url="http://" + base_url + "/status", timeout=(READ_TIMEOUT, RESP_TIMEOUT)
        )
        response.raise_for_status()

        logging.info("response {0}".format(str(response.text)))

        response = json.loads(response.text)

        r_dict[line_id] = dict(id=line_id, state=int(response[str(relay)]))
    except Exception as e:
        logging.error(e)
        logging.error("Can't get line status status. Exception occured. Set status -1")
        r_dict[line_id] = dict(id=line_id, state=-1)

    return r_dict


def check_tank_status(line_id):
    r_dict = {}

    try:
        device_id = LINES[line_id]["device_id"]
        device_url = get_IP_by_local_domain(LINES[line_id]["device_url"])

        response = requests.get(
            url="http://" + device_url, timeout=(READ_TIMEOUT, RESP_TIMEOUT)
        )
        response.raise_for_status()

        logging.info("response {0}".format(str(response.text)))

        #tmp_fix = response.text.replace("upper_tank", '"upper_tank"')

        response = json.loads(response.text)
        if response["device_id"] == device_id:
            r_dict[line_id] = dict(id=line_id, device_state=1)
        else:
            r_dict[line_id] = dict(id=line_id, device_state=-1)

    except Exception as e:
        logging.exception(e)
        logging.error("Can't check tank status. Exception occured. Set status -1")
        r_dict[line_id] = dict(id=line_id, device_state=-1)

    return r_dict
