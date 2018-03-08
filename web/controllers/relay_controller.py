#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time
import RPi.GPIO as GPIO
from itertools import groupby
from operator import itemgetter
from helpers import sqlite_database as database
from helpers.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

PUMP_PIN = 12
RAIN_PIN = 21
RAIN_BUCKET_ITERATION = 1
# 1,2,3 goes to light activities
EXCEPT_PINS = [1, 2, 3, PUMP_PIN, RAIN_PIN]
BRANCHES = []


def setup_relays():
    """Fill up settings array to save settings for branches."""
    try:
        groups = database.select(database.QUERY[mn()])
        # QUERY['get_settings'] = "SELECT number, name, time, intervals, time_wait, start_time, line_type, base_url, pump_enabled from lines where line_type='power_outlet' order by number"
        groups.sort(key=itemgetter(9))

        grouped = []
        for key, group in groupby(groups, itemgetter(9)):
            grouped.append(list([list(thing) for thing in group]))
        for row in grouped:
            print(row)

    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))

setup_relays()

BRANCHES = [
    {'id': 1, 'relay_num': 1, 'state': -1, 'mode': GPIO.OUT},
    {'id': 1, 'relay_num': 1, 'state': -1, 'mode': GPIO.OUT},
    {'id': 2, 'relay_num': 2, 'state': -1, 'mode': GPIO.OUT},
    {'id': 3, 'relay_num': 3, 'state': -1, 'mode': GPIO.OUT},
    {'id': 4, 'relay_num': 4, 'state': -1, 'mode': GPIO.OUT},
    {'id': 5, 'relay_num': 5, 'state': -1, 'mode': GPIO.OUT},
    {'id': 6, 'relay_num': 6, 'state': -1, 'mode': GPIO.OUT},
    {'id': 7, 'relay_num': 7, 'state': -1, 'mode': GPIO.OUT},
    {'id': 8, 'relay_num': 8, 'state': -1, 'mode': GPIO.OUT},
    {'id': 9, 'relay_num': 9, 'state': -1, 'mode': GPIO.OUT},
    {'id': 10, 'relay_num': 10, 'state': -1, 'mode': GPIO.OUT},
    {'id': 11, 'relay_num': 11, 'state': -1, 'mode': GPIO.OUT},
    {'id': 12, 'relay_num': 12, 'state': -1, 'mode': GPIO.OUT},
    {'id': 13, 'relay_num': 13, 'state': -1, 'mode': GPIO.OUT},
    {'id': 14, 'relay_num': 14, 'state': -1, 'mode': GPIO.OUT},
    {'id': 15, 'relay_num': 15, 'state': -1, 'mode': GPIO.OUT},
    {'id': 16, 'relay_num': 16, 'state': -1, 'mode': GPIO.OUT},
    {'id': 17, 'relay_num': PUMP_PIN, 'state': -1, 'mode': GPIO.OUT},
]


def rissing(channel):
    """Fillup rain table"""
    global RAIN_BUCKET_ITERATION
    time.sleep(0.005)
    if GPIO.input(RAIN_PIN) == 1:
        logging.info("Rain bucket movment {0} detected.".format(RAIN_BUCKET_ITERATION))
        RAIN_BUCKET_ITERATION += 1
        time.sleep(1)

        database.update(database.QUERY[mn()].format(RAIN_CONSTANT_VOLUME))


GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

for branch in BRANCHES:
    GPIO.setup(branch['relay_num'], branch['mode'], initial=GPIO.LOW)

GPIO.setup(RAIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(RAIN_PIN, GPIO.RISING, callback=rissing, bouncetime=200)


def detect_pin(pin):
    return '{0:04b}'.format(pin)


def on(pin):
    """Set pin to hight state."""
    try:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        return GPIO.input(pin)
    except Exception as e:
        logging.error("Exception occured when turning on {0} pin. {1}".format(pin, e))
        GPIO.cleanup()
        return -1


def off(pin):
    """Set pin to low state."""
    try:
        GPIO.output(pin, GPIO.LOW)
        return GPIO.input(pin)
    except Exception as e:
        logging.error("Exception occured when turning off {0} pin. {1}".format(pin, e))
        GPIO.cleanup()
        return -1


def check_if_no_active():
    """Check if any of branches is active now."""
    try:
        for branch in BRANCHES:
            # pump won't turn off, cause it stays on after branch off
            if branch['relay_num'] in EXCEPT_PINS:
                continue

            state = GPIO.input(branch['relay_num'])
            if state == GPIO.HIGH:
                logging.info("branch {0} is active".format(branch['id']))
                return False

        logging.info("No active branch")
        return True
    except Exception as e:
        logging.error("Exception occured when checking active {0}".format(e))
        GPIO.cleanup()
        raise e


def form_pins_state():
    """Form returns arr of dicts."""
    try:
        for branch in BRANCHES:
            branch['state'] = GPIO.input(branch['relay_num'])

        logging.debug("Pins state are {0}".format(str(BRANCHES)))

        return BRANCHES
    except Exception as e:
        logging.error("Exception occured during forming of branches status. {0}".format(e))
        GPIO.cleanup()
        return None


def branch_on(branch_id=None, branch_alert=None, pump_enable=True):
    """Turn on branch by id."""
    if (branch_id is None):
        logging.error("No branch id")
        return None

    if (branch_alert is None):
        logging.error("No branch alert time")
        return None

    on(BRANCHES[branch_id]['relay_num'])

    if pump_enable is False:
        logging.info("Pump won't be turned on with {0} branch id".format(branch_id))
    else:
        on(PUMP_PIN)
        logging.info("Pump turned on with {0} branch id".format(branch_id))

    return form_pins_state()


def branch_off(branch_id=None, pump_enable=True):
    """Turn off branch by id."""
    if (branch_id is None):
        logging.error("No branch id")
        return None

    off(BRANCHES[branch_id]['relay_num'])

    if pump_enable is True and check_if_no_active():
        off(PUMP_PIN)
        logging.info("Pump turned off with {0} branch id".format(branch_id))
    else:
        logging.info("Pump won't be turned off with {0} branch id".format(branch_id))

    return form_pins_state()


def branch_status():
    """Return status of raspberryPi relay."""
    try:
        return form_pins_state()
    except Exception as e:
        logging.error(e)
        logging.error("Can't get raspberryPi status. Exception occured")
        return None
