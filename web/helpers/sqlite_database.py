import sqlite3
import logging
import json
from helpers.redis import *
from helpers.common import *
from itertools import groupby
from operator import itemgetter
import ast


QUERY = {}
QUERY['get_next_active_rule'] = (
    "SELECT l.id, l.line_id, l.rule_id, l.timer as \"[timestamp]\", l.interval_id, l.time, li.name "
    "FROM life AS l, lines as li "
    "WHERE l.state = 1 AND l.active=1 AND l.line_id={0} AND li.number = l.line_id AND timer>=datetime('now', 'localtime') "
    "ORDER BY timer LIMIT 1")

QUERY['get_last_start_rule'] = (
    "SELECT l.id, l.line_id, l.rule_id, l.timer as \"[timestamp]\", l.interval_id "
    "FROM life AS l "
    "WHERE l.state = 2 AND l.active=1 AND l.rule_id = 1 AND l.line_id={0} AND timer<=datetime('now', 'localtime') "
    "ORDER BY timer DESC LIMIT 1")

QUERY['history'] = (
    "SELECT l.interval_id, li.name, l.date, l.timer as \"[timestamp]\", l.active, l.time "
    "FROM life as l, lines as li "
    "WHERE l.rule_id = 1 AND (date(l.timer) BETWEEN date('now', 'localtime') AND date('now', 'localtime', '+{0} day')) AND l.line_id = li.number AND l.state = 1 AND l.active = 1 "
    "ORDER BY l.timer DESC")

QUERY['ongoing_rules'] = (
    "SELECT r.id, r.line_id, r.time, r.intervals, r.time_wait, r.repeat_value, r.date_time_start, r.end_date, r.active, l.name, r.rule_id "
    "FROM ongoing_rules as r, lines as l WHERE r.line_id = l.number AND (date(r.end_date) >= date('now', 'localtime')) "
    "EXCEPT select r.id, r.line_id, r.time, r.intervals, r.time_wait, r.repeat_value, r.date_time_start, r.end_date, r.active, l.name, r.rule_id "
    "FROM ongoing_rules as r, lines as l WHERE r.line_id = l.number and date(r.date_time_start) = date('now', 'localtime') "
    "and date(r.date_time_start) = date(r.end_date) and time('now', 'localtime') >= time(r.date_time_start) ORDER BY r.date_time_start;")

QUERY['add_ongoing_rule'] = (
    "INSERT INTO ongoing_rules(line_id, time, intervals, time_wait, repeat_value, date_time_start, "
    "end_date, active, rule_id) "
    "VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', '{6}', {7}, '{8}')")

QUERY['update_rules_from_ongoing_rules_select_id'] = (
    "SELECT * FROM ongoing_rules "
    "WHERE rule_id = '{0}'")

QUERY['update_rules_from_ongoing_rules_update_ongoing_rule'] = (
    "UPDATE ongoing_rules "
    "SET line_id = {1}, time = {2}, intervals = {3}, "
    "time_wait = {4}, repeat_value = {5}, date_time_start = {6}, "
    "end_date = {7}, active = {8}"
    "WHERE rule_id = '{0}'")

QUERY['update_rules_from_ongoing_rules_delete_ongoing_rule'] = (
    "DELETE FROM ongoing_rules WHERE rule_id = '{0}'")

QUERY['update_rules_from_ongoing_rules_remove_from_life'] = (
    "DELETE FROM life WHERE ongoing_rule_id = '{0}' AND timer >= datetime('now', 'localtime')")

QUERY['remove_ongoing_rule_delete_ongoing_rule'] = QUERY['update_rules_from_ongoing_rules_delete_ongoing_rule']

QUERY['remove_ongoing_rule_remove_from_life'] = QUERY['update_rules_from_ongoing_rules_remove_from_life']

QUERY['update_rules_from_ongoing_rules_add_rule_to_life'] = (
    "INSERT INTO life(line_id, rule_id, state, date, timer, interval_id, time, ongoing_rule_id) "
    "VALUES ({0}, {1}, {2}, '{3}', '{4}', '{5}', {6}, '{7}')")

QUERY['add_rule'] = (
    "INSERT INTO life(line_id, rule_id, state, date, timer, interval_id, time) "
    "VALUES ({0}, {1}, {2}, '{3}', '{4}', '{5}', {6})")

QUERY['activate_branch_1'] = (
    "INSERT INTO life(line_id, rule_id, state, date, timer, interval_id, time) "
    "VALUES ({0}, {1}, {2}, '{3}', '{4}', '{5}', {6})")

QUERY['activate_branch_2'] = (
    "SELECT l.id, l.line_id, l.rule_id, l.timer, l.interval_id, l.time, li.name "
    "FROM life as l, lines as li "
    "WHERE l.id = {0} AND li.number = l.line_id")

QUERY['deactivate_branch_1'] = (
    "UPDATE life "
    "SET state=4 "
    "WHERE interval_id = '{0}' AND state = 1")

QUERY['deactivate_branch_2'] = (
    "INSERT INTO life(line_id, rule_id, state, date, timer, interval_id) "
    "VALUES ({0}, {1}, {2}, '{3}', '{4}', '{5}')")

QUERY['enable_rule'] = "UPDATE life SET state=2 WHERE id={0}"
QUERY['enable_rule_canceled_by_rain'] = "UPDATE life SET state=5 WHERE id={0}"

QUERY['activate_ongoing_rule_ongoing'] = "UPDATE ongoing_rules SET active=1 WHERE rule_id='{0}'"
QUERY['activate_ongoing_rule_life'] = "UPDATE life SET active=1 WHERE ongoing_rule_id='{0}'"

QUERY['deactivate_ongoing_rule_ongoing'] = "UPDATE ongoing_rules SET active=0 WHERE rule_id='{0}'"
QUERY['deactivate_ongoing_rule_life'] = "UPDATE life SET active=0 WHERE ongoing_rule_id='{0}'"

QUERY['edit_ongoing_rule_ongoing'] = (
    "UPDATE ongoing_rules "
    "SET line_id = {0}, time = {1}, intervals = {2}, "
    "time_wait = {3}, repeat_value={4}, "
    "date_time_start='{5}', end_date = '{6}' "
    "WHERE rule_id = '{7}'")

QUERY['remove_rule'] = "DELETE from life WHERE id={0}"

QUERY['cancel_rule_1'] = "SELECT l.interval_id, li.name, l.ongoing_rule_id FROM life AS l, lines AS li WHERE l.interval_id = '{0}' AND l.line_id = li.number"
QUERY['cancel_rule_2'] = "UPDATE life SET state = 4 WHERE interval_id = '{0}' AND state = 1"
QUERY['cancel_rule_select_ongoing_rule'] = "SELECT * FROM life where ongoing_rule_id='{0}' AND state = 1 AND timer>=datetime('now', 'localtime') "
QUERY['cancel_rule_delete_ongoing_rule'] = "DELETE FROM ongoing_rules WHERE rule_id = '{0}'"

QUERY['get_settings'] = (
    "SELECT l.number, l.name, l.time, l.intervals, l.time_wait, l.start_time, "
    "l.line_type, l.base_url, l.pump_enabled, l.is_pump, lg.id, lg.name, l.relay_num "
    "FROM lines AS l, line_groups as lg where l.group_id = lg.id ORDER BY l.number")

QUERY['setup_lines_lines'] = (
    "SELECT l.number, lg.s0, lg.s1, lg.s2, lg.s3, "
    "lg.en, l.pump_enabled, l.pin, lg.multiplex, l.relay_num, l.is_pump, l.is_except, "
    "l.group_id, l.pump_pin, l.name, lg.name, l.base_url "
    "FROM lines AS l, line_groups as lg where l.group_id = lg.id ORDER BY l.number")

QUERY['setup_lines_remote_control'] = (
    "SELECT l.number, l.relay_num, l.is_pump, l.is_except, "
    "l.group_id, l.name, lg.name, l.base_url "
    "FROM lines AS l, line_groups as lg where l.group_id = lg.id ORDER BY l.number"
    )

QUERY['setup_sensors_datalogger']  = (
    "SELECT l.number, l.line_type, l.base_url "
    "FROM lines AS l "
    "WHERE l.line_type like '%sensor' "
    "ORDER BY l.number"
    )

QUERY['setup_lines_datalogger']  = (
    "SELECT l.number, l.moisture_id "
    "FROM lines AS l "
    "WHERE l.moisture_id is not NULL "
    "ORDER BY l.number"
    )


QUERY['setup_lines_greenlines'] = (
    "SELECT l.number, l.base_url "
    "FROM lines AS l "
    "ORDER BY l.number"
    )

QUERY['temp_sensors_air'] = (
    "INSERT into temperature (line_id, temp, hum, datetime) values ({0}, '{1}', '{2}', '{3}')"
    )

QUERY['temp_sensors_ground'] = (
    "INSERT into temperature (line_id, temp, datetime) values ({0}, '{1}', '{2}')"
    )


QUERY['enable_rule_cancel_interval'] = "UPDATE life SET state={1} WHERE state=1 AND interval_id='{0}'"

QUERY['rissing'] = "INSERT INTO rain (volume) VALUES ({0})"

QUERY['get_rain_volume'] = "SELECT sum(volume) from rain where datetime >= datetime('now', 'localtime', '-{0} hours');"
QUERY['moisture_sensors'] = (
    "INSERT INTO moisture(line_id, value) "
    "VALUES ({0}, {1})")

QUERY['get_moisture'] = (
    "SELECT line_id, value, datetime FROM moisture WHERE datetime >= datetime('now', 'localtime', '-23 hours');")

QUERY['get_temperature'] = (
    "SELECT t.line_id, t.temp, t.hum, l.name, l.line_type, t.datetime from temperature as t, lines as l where t.line_id = l.number and datetime >= datetime('now', 'localtime', '-{0} days');")

QUERY['get_temperature2'] = (
    "SELECT t.line_id, t.temp, t.hum, l.name, l.line_type, t.datetime from temperature as t, lines as l where t.line_id = l.number and datetime >= datetime('now', 'localtime', '-{0} days') "
    "order by t.datetime DESC limit 100;")

QUERY['get_app_settings'] = "SELECT short_name, json_value from settings"

QUERY['set_app_settings'] = "update settings set json_value=\"{0}\" where short_name = {1}"

QUERY['migrate_data'] = 'select * from temperature'
QUERY['migrate_data_insert'] = 'select * from temperature'


# executes query and returns fetch* result
def select(query, method='fetchall'):
    """Use this method in case you need to get info from database."""
    conn = None
    try:
        conn = sqlite3.connect('/var/sqlite_db/smart_system.sql', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # execute our Query
        cursor.execute(query)
        logging.debug("db request '{0}' executed".format(query))
        return getattr(cursor, method)()
    except Exception as e:
        logging.error("Error while performing operation with database: '{0}'. query: '{1}'".format(e, query))
        return None
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception as e:
            logging.error("Error while closing connection with database: {0}".format(e))


# executes query and returns fetch* result
def update(query):
    """Doesn't have fetch* methods. Returns lastrowid after database insert command."""
    conn = None
    lastrowid = -1
    try:
        conn = sqlite3.connect('/var/sqlite_db/smart_system.sql', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        # execute our Query
        cursor.execute(query)
        conn.commit()
        logging.debug("db request '{0}' executed".format(query))
        lastrowid = cursor.lastrowid
        return lastrowid
    except Exception as e:
        logging.error("Error while performing operation with database: '{0}'. query: '{1}'".format(e, query))
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception as e:
            logging.error("Error while closing connection with database: {0}".format(e))
            return None


def get_next_active_rule(line_id):
    """Return nex active rule."""
    query = QUERY[mn()].format(line_id)
    res = select(query, 'fetchone')
    if res is None:
        return None

    logging.debug("Next active rule retrieved for line id {0}".format(line_id))
    return {'id': res[0], 'line_id': res[1], 'rule_id': res[2], 'user_friendly_name': res[6], 'timer': res[3], 'interval_id': res[4], 'time': res[5]}


def get_last_start_rule(line_id):
    """Return last compeled start irrigation rule."""
    query = QUERY[mn()].format(line_id)
    res = select(query, 'fetchone')
    if res is None:
        return None

    logging.debug("Last completed rule retrieved for line id {0}".format(line_id))
    return {'id': res[0], 'line_id': res[1], 'rule_id': res[2], 'timer': res[3], 'interval_id': res[4]}


def get_rain_volume():
    """Return volume of rain mm/m^2"""
    rain = select(QUERY[mn()].format(RAIN_HOURS))[0][0]
    if rain is None:
        rain = 0

    return round(rain, 2)


def get_temperature2():
    try:
        list_arr = select(QUERY[mn()].format(TEMP_DAYS))
        if list_arr is not None:
            list_arr.sort(key=itemgetter(5))

        grouped = {}
        for key, group in groupby(list_arr, itemgetter(5)):
            grouped[key] = [list(thing) for thing in group]
        logging.info(grouped)
        return grouped

            #             round(thing[1], 2),
            #             round(thing[1], 2),
            #             round(thing[1], 2),
            #             int(convert_to_datetime(thing[2]).strftime('%H'))])
            #     grouped[key] = {}
            #     grouped[key]['new'] = _list

            # for key, value in grouped.items():
            #     new_list = list()
            #     for _key, _group in groupby(value['new'], itemgetter(1)):
            #         _sum = 0
            #         _len = 0
            #         for thing in _group:
            #             _sum += thing[0]
            #             _len += 1
            #         new_list.append(
            #             dict(hours=_key, val=round(_sum / _len, 2)))
            #     grouped[key]['new'] = new_list
            #     grouped[key]['base'] = 60

            # for key, value in grouped.items():
            #     del value['new'][::2]
    except Exception as e:
        logging.error(e)


def get_temperature():
    """Return volume of rain mm/m^2"""
    list_arr = select(QUERY[mn()].format(TEMP_DAYS))

    if list_arr is not None:
        list_arr.sort(key=itemgetter(0))

        grouped = {}
        for key, group in groupby(list_arr, itemgetter(0)):
            grouped[key] = {
            'sensor_id': key,
            # 'sensor_name': 
            # 'sensor_type': 
            'values': [list(thing) for thing in group]
            }

        for s_id, sensor in grouped.items():
            sensor['values'].sort(key=itemgetter(5), reverse=True)

    return grouped


def get_app_settings():
    list_arr = select(QUERY[mn()])
    settings = {}
    for row in list_arr:
        settings[row[0]] = ast.literal_eval(row[1])

    return settings


def set_app_settings(settings):
    "update settings set json_value=json({0}) where short_name = {1}"
    logging.info(settings)
    for k, v in settings.items():
        update(QUERY[mn()].format(v, json.dumps(k)))

    return True
