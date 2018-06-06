#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
twoup = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
from flask import Flask
from flask import jsonify, request, render_template
from flask.ext.cache import Cache
import datetime
from itertools import groupby
from operator import itemgetter
from collections import OrderedDict
from common import sqlite_database as database
from common.redis import *
from common.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

CACHE_TIMEOUT = 600


def update_all_rules():
    """Set next active rules for all branches."""
    try:
        for i in range(1, len(RULES_FOR_BRANCHES)):
            set_next_rule_to_redis(i, database.get_next_active_rule(i))
        logging.info("Rules updated")
    except Exception as e:
        logging.error("Exeption occured while updating all rules. {0}".format(e))


def get_settings():
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

        global APP_SETTINGS
        APP_SETTINGS = database.get_app_settings()
        logging.info("APP settings: {0}".format(str(APP_SETTINGS)))

    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))


@app.route("/")
@cache.cached(timeout=CACHE_TIMEOUT)
def index():
    """Index page."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'irrigation' and item['is_pump'] == 0:
            branch_list.append({
                'id': item['branch_id'],
                'group_id': item['group_id'],
                'group_name': item['group_name'],
                'is_pump': item['is_pump'],
                'name': item['name'],
                'default_time': item['time'],
                'default_interval': item['intervals'],
                'default_time_wait': item['time_wait'],
                'start_time': item['start_time']})

    branch_list.sort(key=itemgetter('group_id'))
    grouped = {}
    for key, group in groupby(branch_list, itemgetter('group_id')):
        grouped[key] = (list([thing for thing in group]))

    return render_template('index.html', my_list=grouped)


@app.route("/pumps")
@cache.cached(timeout=CACHE_TIMEOUT)
def pumps():
    """Index page."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'irrigation' and item['is_pump'] == 1:
            branch_list.append({
                'id': item['branch_id'],
                'group_id': item['group_id'],
                'group_name': item['group_name'],
                'is_pump': item['is_pump'],
                'name': item['name'],
                'default_time': item['time'],
                'default_interval': item['intervals'],
                'default_time_wait': item['time_wait'],
                'start_time': item['start_time']})

    branch_list.sort(key=itemgetter('group_name'))
    grouped = {}
    for key, group in groupby(branch_list, itemgetter('group_name')):
        grouped[key] = (list([thing for thing in group]))

    return render_template('pumps.html', my_list=grouped)


@app.route("/greenhouse")
@cache.cached(timeout=CACHE_TIMEOUT)
def greenhouse():
    """Index page."""
    my_list = {}
    my_list['sensors'] = database.get_temperature()

    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'greenhouse':
            branch_list.append({
                'id': item['branch_id'],
                'group_id': item['group_id'],
                'group_name': item['group_name'],
                'is_pump': item['is_pump'],
                'name': item['name'],
                'default_time': item['time'],
                'default_interval': item['intervals'],
                'default_time_wait': item['time_wait'],
                'start_time': item['start_time']})

    branch_list.sort(key=itemgetter('id'))
    my_list['lines'] = branch_list
    my_list['temperature'] = database.get_temperature2()

    return render_template('greenhouse.html', my_list=my_list)


@app.route("/branch_settings")
@cache.cached(timeout=CACHE_TIMEOUT)
def branch_settings():
    """Return branch names."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'irrigation':
            branch_list.append({
                'id': item['branch_id'],
                'name': item['name'],
                'default_time': item['time'],
                'default_interval': item['intervals'],
                'default_time_wait': item['time_wait'],
                'start_time': item['start_time']})

    return jsonify(list=branch_list)


@app.route("/tank")
@cache.cached(timeout=CACHE_TIMEOUT)
def tank():
    """Return branch names."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'tank':
            branch_list.append({
                'id': item['branch_id'],
                'name': item['name'],
                'default_time': item['time']})

    return render_template('tank.html', my_list=branch_list)


@app.route("/lighting")
@cache.cached(timeout=CACHE_TIMEOUT)
def lighting():
    """Return branch names."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item['line_type'] == 'lighting':
            branch_list.append({
                'id': item['branch_id'],
                'name': item['name'],
                'default_time': item['time']})

    return render_template('lighting.html', my_list=branch_list)


@app.route("/add_rule")
def add_rule_page():
    if 'add_to_date' in request.args:
        days = int(request.args.get('add_to_date'))

    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item is not None and item['line_type'] == 'irrigation' and item['is_pump'] == 0:
            start_time = convert_to_datetime(item['start_time'])
            branch_list.append({
                'line_id': item['branch_id'],
                'line_name': item['name'],
                'default_time': item['time'],
                'default_interval': item['intervals'],
                'default_time_wait': item['time_wait'],
                'start_time': ("%s:%s" % (start_time.strftime("%H"), start_time.strftime("%M"))),
                'start_date': str(datetime.date.today() + datetime.timedelta(days=days))
            })

    """Add rule page."""
    return render_template('add_rule.html', my_list=branch_list)


@app.route("/history")
def history():
    """Return history page if no parameters passed and only table body if opposite."""
    if 'days' in request.args:
        days = int(request.args.get('days'))
    else:
        days = 7

    # SELECT l.interval_id, li.name, l.date, l.timer as \"[timestamp]\", l.active, l.time 
    grouped_rules = OrderedDict()
    list_arr = database.select(database.QUERY[mn()].format(days), 'fetchall')
    if list_arr is not None:
        list_arr.sort(key=itemgetter(0))

        grouped = []
        for key, group in groupby(list_arr, itemgetter(0)):
            grouped.append(list([list(thing) for thing in group]))

        rules = []
        for intervals in grouped:
            intervals.sort(key=itemgetter(3))
            intervals_quantity = len(intervals)

            time_wait = 0
            if intervals_quantity == 2:
                time_wait = int((intervals[1][3] - intervals[0][3]).total_seconds() / 60 - intervals[0][5])

            row = intervals[0]
            rules.append(dict(
                line_name=row[1],
                date=row[2].strftime('%m/%d/%Y'),
                date_description=form_date_description(row[2]),
                timer=date_handler(row[3]),
                ative=row[4],
                time=row[5],
                intervals=intervals_quantity,
                interval_id=row[0],
                time_wait=time_wait))

        rules.sort(key=itemgetter('date'))
        for key, group in groupby(rules, itemgetter('date')):
            grouped_rules[key] = [thing for thing in group]

        for key, value in grouped_rules.items():
            value.sort(key=itemgetter('timer'))

    return render_template('history.html', my_list=grouped_rules)


@app.route("/ongoing_rules")
def ongoing_rules():
    """Return ongoing_rules.html."""
    list_arr = database.select(database.QUERY[mn()], 'fetchall')
    if (list_arr is None):
        list_arr = []

    rows = []
    now = datetime.datetime.now()
    # SELECT id, line_id, time, intervals, time_wait, repeat_value, dow, date_start, time_start, end_value, end_date, end_repeat_quantity
    for row in list_arr:
        rule_id = row[10]
        line_id = row[1]
        time = row[2]
        intervals = row[3]
        time_wait = row[4]
        repeat_value = row[5]
        date_time_start = row[6]
        end_date = row[7]
        active = row[8]
        name = row[9]
        days = -1

        start_dt = convert_to_datetime(date_time_start)
        end_dt = convert_to_datetime(end_date)

        if start_dt.date() == end_dt.date():
            date_delta = end_dt.date() - now.date()
            if date_delta.days == 0:
                days = 0
            if date_delta.days == 1:
                days = 1

        rows.append({
            'rule_id': rule_id,
            'line_id': line_id,
            'time': time,
            'intervals': intervals,
            'time_wait': time_wait,
            'repeat_value': repeat_value,
            'date_time_start': str(date_time_start),
            'end_date': str(end_date),
            'active': active,
            'line_name': name,
            'days': days})
    template = render_template('ongoing_rules.html', my_list=rows)
    return template


logging.info("Get app settings")
get_settings()
logging.info("Staring app")
