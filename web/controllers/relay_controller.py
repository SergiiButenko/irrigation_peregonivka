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

RAIN_PIN = 21
RAIN_BUCKET_ITERATION = 1
LINES = {}
EN_ENABLED = GPIO.LOW
EN_DISABLED = GPIO.HIGH


def setup_lines():
    """Fill up settings array to save settings for branches."""
    try:
        GPIO.setwarnings(False)
        lines = database.select(database.QUERY[mn() + '_lines'])             
        for row in lines:
            if row[10] != 1:
                key = row[0]
            else:
                key = 'pump'

            LINES[key] = {'id': row[0],
                          's0': row[1],
                          's1': row[2],
                          's2': row[3],
                          's3': row[4],
                          'en': row[5],
                          'pump_enabled': row[6],
                          'pin': row[7],
                          'multiplex': row[8],
                          'relay_num': row[9],
                          'is_pump': row[10],
                          'is_except': row[11],
                          'group_id': row[12],
                          'pump_pin': row[13],
                          'line_name': row[14],
                          'group_name': row[15],
                          'state': -1}

            if LINES[key]['multiplex'] == 1:
                GPIO.setup(LINES[key]['s0'], GPIO.OUT, inital=GPIO.LOW)
                GPIO.setup(LINES[key]['s1'], GPIO.OUT, inital=GPIO.LOW)
                GPIO.setup(LINES[key]['s2'], GPIO.OUT, inital=GPIO.LOW)
                GPIO.setup(LINES[key]['s3'], GPIO.OUT, inital=GPIO.LOW)
                GPIO.setup(LINES[key]['en'], GPIO.OUT, inital=EN_DISABLED)
            else:
                GPIO.setup(LINES[key]['pin'], GPIO.OUT)

            if LINES[key]['pump_enabled'] == 1:
                GPIO.setup(LINES[key]['pump_pin'], GPIO.OUT)

        logging.info(LINES)
        GPIO.setwarnings(True)
    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))


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

setup_lines()

GPIO.setup(RAIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(RAIN_PIN, GPIO.RISING, callback=rissing, bouncetime=200)


def detect_pin_state(r_id):
    return list('{0:04b}'.format(r_id))


def get_relay_num(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def on(pin):
    """Set pin to high state."""
    try:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        return GPIO.input(pin)
    except Exception as e:
        logging.error("Exception occured when turning on {0} pin. {1}".format(pin, e))
        GPIO.cleanup()
        raise(e)


def off(pin):
    """Set pin to low state."""
    try:
        GPIO.output(pin, GPIO.LOW)
        return GPIO.input(pin)
    except Exception as e:
        logging.error("Exception occured when turning off {0} pin. {1}".format(pin, e))
        GPIO.cleanup()
        raise(e)


def on_group(branch_id):
    try:
        en = LINES[branch_id]['en']
        GPIO.output(en, EN_ENABLED)
        logging.info("EN pin {0} enabled".format(en))

        relay = LINES[branch_id]['relay_num']
        _pins = detect_pin_state(relay)
        pins = {LINES[branch_id]['s0']: int(_pins[0]),
                LINES[branch_id]['s1']: int(_pins[1]),
                LINES[branch_id]['s2']: int(_pins[2]),
                LINES[branch_id]['s3']: int(_pins[3])}

        for pin, pin_state in pins.items():
            if pin_state == 1:
                on(pin)
                logging.info("pin {0} enabled".format(pin))
            else:
                off(pin)
                logging.info("pin {0} disabled".format(pin))
    except Exception as e:
        logging.error("Can't turn on group")
        raise(e)


def off_group(branch_id):
    try:
        en = LINES[branch_id]['en']
        GPIO.output(en, EN_DISABLED)
        logging.info("EN pin disabled")

        pins = {LINES[branch_id]['s0']: 0,
                LINES[branch_id]['s1']: 0,
                LINES[branch_id]['s2']: 0,
                LINES[branch_id]['s3']: 0}

        for pin, pin_state in pins.items():
            off(pin)
            logging.info("pin {0} disabled".format(pin))

    except Exception as e:
        raise(e)


def check_if_no_active():
    """Check if any of branches is active now."""
    try:
        for line_id, line in LINES.items():
            # pump won't turn off, cause it stays on after branch off
            if line['is_except'] == 1:
                continue

            if line['multiplex'] == 0:
                state = GPIO.input(line['pin'])
                if state == GPIO.HIGH:
                    logging.info("branch {0} is active".format(line['id']))
                    return False
            else:
                state = GPIO.input(line['en'])
                if state == EN_ENABLED:
                    logging.info("EN pin of {0} group is active".format(line['group_id']))
                    return False

        logging.info("No active branch")
        return True
    except Exception as e:
        logging.error("Exception occured when checking active {0}".format(e))
        GPIO.cleanup()
        raise(e)


def form_pins_state():
    """Form returns arr of dicts."""
    try:
        for line_id, line in LINES.items():
            if line['multiplex'] == 0:
                line['state'] = GPIO.input(line['pin'])
            elif GPIO.input(line['en']) == GPIO.LOW:
                line['state'] = 0
            else:
                s0 = GPIO.input(line['s0'])
                s1 = GPIO.input(line['s1'])
                s2 = GPIO.input(line['s2'])
                s3 = GPIO.input(line['s3'])
                relay_num = get_relay_num([s0, s1, s2, s3])
                if line['relay_num'] == relay_num:
                    line['state'] = 1
                else:
                    line['state'] = 0

        logging.debug("Pins state are {0}".format(str(LINES)))

        return LINES
    except Exception as e:
        logging.error("Exception occured during forming of branches status. {0}".format(e))
        GPIO.cleanup()
        raise(e)


def branch_on(branch_id=None, branch_alert=None, pump_enable=True):
    """Turn on branch by id."""
    if (branch_id is None):
        logging.error("No branch id")
        return None

    if (branch_alert is None):
        logging.error("No branch alert time")
        return None

    if LINES[branch_id]['multiplex'] == 1:
        on_group(branch_id)
    else:
        on(LINES[branch_id]['pin'])

    if LINES[branch_id]['pump_enabled'] == 0:
        logging.info("Pump won't be turned on with {0} branch id".format(branch_id))
    else:
        on(LINES[branch_id]['pump_pin'])
        logging.info("Pump turned on with {0} branch id".format(branch_id))

    return form_pins_state()


def branch_off(branch_id=None, pump_enable=True):
    """Turn off branch by id."""
    if (branch_id is None):
        logging.error("No branch id")
        return None

    if LINES[branch_id]['multiplex'] == 1:
        off_group(branch_id)
    else:
        off(LINES[branch_id]['pin'])

    if LINES[branch_id]['pump_enabled'] == 1 and check_if_no_active():
        off(LINES[branch_id]['pump_pin'])
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
