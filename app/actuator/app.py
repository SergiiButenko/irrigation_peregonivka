from flask import Flask
from be_template.views.view1 import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import time
from datetime import datetime, timedelta
from backend.config import ACTIVE_IP_INTERVAL_MINUTES
from irrigation_helpers import convert_to_datetime, mn

import requests

import sqlite_database as database


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO
)


def get_device_IP_by_line_id(line_id):
    device_id = database.get_device_id_by_line_id(line_id)
    logging.info(f"device_id: {device_id}")
    device = database.get_device_ip(device_id)
    logging.info(f"device: {device}")
    
    if device['last_known_ip'] is None:
        raise ValueError(
            f"No IP found for device id:line_id '{device_id}:{line_id}'")

    _updated = convert_to_datetime(device['updated'])
    if _updated + timedelta(minutes=ACTIVE_IP_INTERVAL_MINUTES) < datetime.now():
        raise Exception(
            f"IP '{device['last_known_ip']}' is outdated for device id:line_id '{device_id}:{line_id}'")

    return device['last_known_ip']



def branch_on(line_id):
    """Turn on branch by id."""
    line = database.get_line_by_id(line_id)
    relay = line["relay_num"]
    base_url = get_device_IP_by_line_id(line_id)
    status = requests.get(
        url="http://" + base_url + "/on",
        params={"relay": relay}
    )
    status.raise_for_status()
    
    r_dict = {}
    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    return r_dict


def branch_off(line_id):
    """Turn off branch by id."""
    r_dict = {}
    line = database.get_line_by_id(line_id)
    
    relay = line["relay_num"]

    base_url = get_device_IP_by_line_id(line_id)
    status = requests.get(
        url="http://" + base_url + "/off",
        params={"relay": relay}
    )
    status.raise_for_status()

    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    return r_dict


def air_sensor(line_id):
    for attempt in range(2):
        try:
            base_url = get_device_IP_by_line_id(line_id)
            response_air = requests.get(
                url="http://" + base_url + "/air_temperature",
            )
            response_air.raise_for_status()

            logging.info("response {0}".format(str(response_air.text)))
            res = json.loads(response_air.text)

            r_dict = {}
            r_dict[line_id] = dict(
                id=line_id, air_temp=res["temp"], air_hum=res["hum"])

            return r_dict
        except Exception as e:
            logging.error(e)
            time.sleep(2)
            continue
    raise Exception("Can't get temperature. Retries limit reached")


def ground_sensor(line_id):
    for attempt in range(2):
        try:
            base_url = get_device_IP_by_line_id(line_id)
            response_air = requests.get(
                url="http://" + base_url + "/ground_temperature",
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


def line_status(line_id):
    """Return status of raspberryPi relay."""
    r_dict = {}

    try:
        base_url = get_device_IP_by_line_id(line_id)
        relay = database.get_line_by_id(line_id)["relay_num"]

        response = requests.get(
            url="http://" + base_url + "/status"
        )
        response.raise_for_status()
        response = json.loads(response.text)

        r_dict[line_id] = dict(id=line_id, state=int(response[str(relay)]))
    except Exception as e:
        logging.error("Error: {}".format(e))
        logging.error(
            "Can't get line status status. Exception occured. Set status -1")
        r_dict[line_id] = dict(id=line_id, state=-1)

    return r_dict


def check_tank_status(line_id):
    r_dict = {}

    try:
        device_id = database.get_line_by_id(line_id)["device_id"]
        linked_device_url = database.get_line_by_id(line_id)["linked_device_url"]

        response = requests.get(
            url="http://" + linked_device_url
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
        logging.error(
            "Can't check tank status. Exception occured. Set status -1")
        r_dict[line_id] = dict(id=line_id, device_state=-1)

    return r_dict
