#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
twoup = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
import inspect
import datetime
import json
from pytz import timezone
from common.common import *
from common import sqlite_database as database
import logging

# For get function name intro function. Usage mn(). Return string with current function name. Instead 'query' will be database.QUERY[mn()].format(....)
mn = lambda: inspect.stack()[1][3]

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def date_handler(obj):
    """Convert datatime to string format."""
    if hasattr(obj, 'isoformat'):
        datetime_obj_utc = obj.replace(tzinfo=timezone('UTC'))
        return datetime_obj_utc.isoformat()
    else:
        raise TypeError


def convert_to_obj(data):
    """Convert to dict."""
    try:
        data = json.loads(data)
    except:
        pass
    return data


def convert_to_datetime(value):
    """Conver data string to datatime object."""
    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        pass

    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    except:
        pass

    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except:
        pass

    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S+00:00")
    except:
        pass

    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    except:
        pass
        # 2017-10-26T15:29:51.685474+00:00

    # 'date_start': '2017-10-31',
    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
    except:
        pass

    # 'date_start': '06:15',
    try:
        value = datetime.datetime.strptime(value, "%H:%M")
    except:
        pass

    # 2018-01-23 22:00:00
    try:
        value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except:
        pass

    return value


def date_hook(json_dict):
    """Convert str to datatime object."""
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = convert_to_datetime(value)
        except:
            pass

    return json_dict


def get_weekday(date):
    """Conver date into day of week in UA."""
    week = ['Понеділок',
            'Вівторок',
            'Середа',
            'Четверг',
            'П\'ятниця',
            'Субота',
            'Неділя']

    return week[date.weekday()]


def get_month(date):
    """Used in hostory request."""
    monthes = ['Січня',
               'Лютого',
               'Березня',
               'Квітня',
               'Травня',
               'Червня',
               'Липня',
               'Серпня',
               'Вересня',
               'Жовтня',
               'Листопада',
               'Грудня']
    return monthes[date.month - 1]


def form_date_description(date):
    """Used in hostory request."""
    date = convert_to_datetime(date)
    now = datetime.date.today()
    delta = date - now

    if delta.days == -1:
        return 'Вчора, ' + get_weekday(date)

    if delta.days == 0:
        return 'Сьогодні, ' + get_weekday(date)

    if delta.days == 1:
        return 'Завтра, ' + get_weekday(date)

    return "{0}, {1} {2}".format(get_weekday(date), date.strftime('%d'), get_month(date))


def get_settings():
    BRANCHES_SETTINGS = {}
    APP_SETTINGS = {}
    """Fill up settings array to save settings for branches."""
    try:
        branches = database.select(database.QUERY[mn()])
        for row in branches:
            branch_id = row[0]
            name = row[1]
            time = row[2]
            intervals = row[3]
            time_wait = row[4]
            start_time = row[5]
            line_type = row[6]
            base_url = row[7]
            pump_enabled = row[8]
            is_pump = row[9]
            group_id = row[10]
            group_name = row[11]
            relay_num = row[12]

            BRANCHES_SETTINGS[branch_id] = {
                'branch_id': branch_id,
                'name': name,
                'time': time,
                'intervals': intervals,
                'time_wait': time_wait,
                'start_time': start_time,
                'line_type': line_type,
                'base_url': base_url,
                'pump_enabled': True if pump_enabled == 1 else False,
                'is_pump': is_pump,
                'group_id': group_id,
                'group_name': group_name,
                'relay_num': relay_num
            }

            logging.debug("{0} added to settings".format(str(BRANCHES_SETTINGS[branch_id])))

        APP_SETTINGS = database.get_app_settings()
        logging.info("APP settings: {0}".format(str(APP_SETTINGS)))

        return BRANCHES_SETTINGS, APP_SETTINGS

    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))
