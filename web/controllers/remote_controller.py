#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time
from itertools import groupby
from operator import itemgetter
from helpers import sqlite_database as database
from helpers.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

LINES = {}


def setup_lines_remote_control():
    """Fill up settings array to save settings for branches."""
    try:
        lines = database.select(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            if row[7] is None:
                continue

            LINES[key] = {'id': row[0],
                             'relay_num': row[1],
                             'is_pump': row[2],
                             'is_except': row[3],
                             'group_id': row[4],
                             'line_name': row[5],
                             'group_name': row[6],
                             'base_url': row[7],
                             'state': -1}

        logging.info(LINES)
    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))

setup_lines_remote_control()


def on(line_id):
    """Set pin to high state."""
    try:
        relay = LINES[line_id]['relay_num']
        base_url = LINES[line_id]['base_url']
        response_on = requests.get(url='http://' + base_url + '/on', params={'relay': relay, 'relay_alert': time_min}, timeout=(5, 5))
        logging.info('response {0}'.format(str(response_on.text)))

        return json.loads(response_on.text)

    except Exception as e:
        logging.error("Exception occured when turning on {0} relay. {1}".format(relay, e))
        raise e


def off(line_id):
    """Set pin to low state."""
    try:
        relay = LINES[line_id]['relay_num']
        base_url = LINES[line_id]['base_url']
        response_off = requests.get(url='http://' + base_url + '/off', params={'relay': relay}, timeout=(5, 5))
        logging.info('response {0}'.format(str(response_off.text)))

        return json.loads(response_off.text)
    except Exception as e:
        logging.error("Exception occured when turning off {0} relay. {1}".format(relay, e))
        raise e


def air_s(line_id):
    try:
        base_url = LINES[line_id]['base_url']
        response_air = requests.get(url='http://' + base_url + '/air_status', timeout=(5, 5))
        logging.info('response {0}'.format(str(response_air.text)))
        res = json.loads(response_air.text)

        r_dict = {}
        r_dict[line_id] = dict(id=line_id, air_temp=res['temp'], air_hum=res['hum'])

        return r_dict
    except Exception as e:
        raise e


def ground_s(line_id):
    try:
        base_url = LINES[line_id]['base_url']
        response_air = requests.get(url='http://' + base_url + '/ground_status', timeout=(5, 5))
        logging.info('response {0}'.format(str(response_air.text)))
        res = json.loads(response_air.text)

        r_dict = {}
        r_dict[line_id] = dict(id=line_id, ground_temp=res['temp'])

        return r_dict
    except Exception as e:
        raise e


def branch_on(line_id=None, line_alert=None):
    """Turn on branch by id."""
    if (line_id is None):
        logging.error("No branch id")
        return None

    if (line_alert is None):
        logging.error("No branch alert time")
        return None

    relay = LINES[line_id]['relay_num']
    status = on(LINES[line_id]['id'])
    r_dict = {}
    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    return r_dict


def branch_off(line_id=None):
    """Turn off branch by id."""
    if (line_id is None):
        logging.error("No branch id")
        return None

    relay = LINES[line_id]['relay_num']
    status = off(LINES[line_id]['id'])
    r_dict = {}
    r_dict[line_id] = dict(id=line_id, state=int(status[str(relay)]))

    return r_dict


def air_sensor(line_id=None):
    if line_id is None:
        logging.error('No line id')
        return None

    return air_s()


def ground_sensor(line_id=None):
    if line_id is None:
        logging.error('No line id')
        return None

    return ground_s()


def line_status(line_id):
    """Return status of raspberryPi relay."""
    try:
        base_url = LINES[line_id]['base_url']
        relay = LINES[line_id]['relay_num']
        response = requests.get(url='http://' + base_url + '/status', timeout=(5, 5))
        logging.info('response {0}'.format(str(response.text)))

        response = json.loads(response.text)

        r_dict = {}
        r_dict[line_id] = dict(id=line_id, state=int(response[str(relay)]))

        return r_dict

    except Exception as e:
        logging.error(e)
        logging.error("Can't get line status status. Exception occured")
        return None
