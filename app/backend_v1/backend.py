#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import time
import uuid
from itertools import groupby
from operator import itemgetter

import eventlet
import redis_provider
import requests
import sqlite_database as database
from flask import Flask, abort, jsonify, render_template, request
from flask_caching import Cache
from flask_socketio import SocketIO, emit
from irrigation_helpers import convert_to_datetime, convert_to_obj, date_handler, mn

from backend import config, remote_controller

eventlet.monkey_patch()
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

logging.getLogger("socketio").setLevel(logging.ERROR)
logging.getLogger("engineio").setLevel(logging.ERROR)

app = Flask(__name__)
socketio = SocketIO(
    app, async_mode="eventlet", engineio_logger=False, message_queue="redis://redis", cors_allowed_origins="*"
)

cache = Cache(app, config={"CACHE_TYPE": "simple"})

CACHE_TIMEOUT = 600


@socketio.on_error_default
def error_handler(e):
    """Handle error for websockets."""
    logging.error(
        "error_handler for socketio. An error has occurred: " + str(e))


def send_message(channel, data):
    """Enclose emit method into try except block."""
    try:
        socketio.emit(channel, data)
        logging.debug("Message was sent.")
        logging.debug(data)
    except Exception as e:
        logging.error(e)
        logging.error("Can't send message. Exeption occured")


def send_branch_status_message(data):
    """Convert data in order to send data object."""
    send_message(
        "branch_status", {"data": json.dumps(
            {"branches": data}, default=date_handler)}
    )


def send_history_change_message():
    """Convert data in order to send data object."""
    send_message("refresh_history", {"data": {"refresh": 1}})


@app.route("/")
def main():
    return jsonify(line_settings=database.get_settings()[0], app_settings=database.get_settings()[1])


@app.route("/branch_settings")
@cache.cached(timeout=CACHE_TIMEOUT)
def branch_settings():
    """Return branch names."""
    branch_list = []
    for item_id, item in database.get_settings()[0].items():
        if item["line_type"] == "irrigation":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                    "default_interval": item["intervals"],
                    "default_time_wait": item["time_wait"],
                    "start_time": item["start_time"],
                    "is_pump": item["is_pump"],
                }
            )

    return jsonify(list=branch_list)


@app.route("/lighting_settings")
@cache.cached(timeout=CACHE_TIMEOUT)
def lighting_settings():
    """Return branch names."""
    branch_list = []
    for item_id, item in database.get_settings()[0].items():
        if item["line_type"] == "lighting":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                }
            )

    return jsonify(list=branch_list)


@app.route("/tank_settings")
@cache.cached(timeout=CACHE_TIMEOUT)
def tank_settings():
    """Return branch names."""
    branch_list = []
    for item_id, item in database.get_settings()[0].items():
        if item["line_type"] == "tank":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                    "start_time": item["start_time"],
                }
            )

    return jsonify(list=branch_list)


@app.route("/greenhouse_settings")
@cache.cached(timeout=CACHE_TIMEOUT)
def greenhouse_settings():
    """Return branch names."""
    branch_list = []
    for item_id, item in database.get_settings()[0].items():
        if item["line_type"] == "greenhouse":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                }
            )

    return jsonify(list=branch_list)


@app.route("/plan", methods=["POST"])
def plan():
    income_lines = request.json["lines"]
    income_timer = request.json["timer"]

    income_lines_id = []
    for line_id, line in income_lines.items():
        income_lines_id.append(int(line_id))

    logging.info("Income lines: {0}".format(str(income_lines)))

    # setup lines array
    line_list = []
    for line_id, line in database.get_settings()[0].items():
        if line_id in income_lines_id:
            _line = income_lines[str(line_id)]
            line_list.append(
                {
                    "id": line_id,
                    "name": line["name"],
                    "default_time": int(_line["time"]) if _line["time"] else 0,
                    "default_interval": int(_line["intervals"]) if _line["intervals"] else 0,
                    "default_time_wait": int(_line["time_wait"]) if _line["time_wait"] else 0
                }
            )

    logging.info("line_list: {0}".format(str(line_list)))

    if income_timer == 0:
        start_point = datetime.datetime.now()
        delta_minutes = 0
    elif income_timer == 1:
        last_ongoing_rule = database.get_last_ongoing_rule()

        if last_ongoing_rule is None:
            start_point = datetime.datetime.now()
            delta_minutes = 0
        else:
            start_point = last_ongoing_rule["end_timestamp"]
            delta_minutes = 2 * (
                last_ongoing_rule["time"] * last_ongoing_rule["intervals"]
                + last_ongoing_rule["time_wait"] *
                (last_ongoing_rule["intervals"] - 1 or 1)
            )
    else:
        start_point = datetime.datetime.now()
        # 1 hour has value 2 in dropdown.
        delta_minutes = (income_timer - 1) * 60

    start_time = start_point + datetime.timedelta(minutes=delta_minutes)

    rules = []
    for line in line_list:
        new_rule = {
            "line_id": int(line["id"]),
            "time": int(line["default_time"]),
            "intervals": int(line["default_interval"]),
            "time_wait": int(line["default_time_wait"]),
            "repeat_value": 4,  # comes from ongoing rule. equal to ONE TIME
            "date_start": start_time,
            "time_start": start_time,
            "date_time_start": start_time,
            "end_date": start_time,
            "active": 1,
            "rule_id": str(uuid.uuid4()),
            "days": -1,
            "line_name": line["name"],
        }
        rules.append(new_rule)
        new_delta = 2 * (
            new_rule["time"] * new_rule["intervals"]
            + new_rule["time_wait"] * (new_rule["intervals"] - 1 or 1)
        )
        start_time = start_time + datetime.timedelta(minutes=new_delta)

    logging.info("rules: {0}".format(str(rules)))

    return json.dumps({"status": "OK"})


def form_responce_for_branches(payload):
    """Return responce with rules."""
    try:
        res = {}
        payload = convert_to_obj(payload)
        for line_id, line in payload.items():
            status = line["state"]
            line_id = line["id"]
            line_group = database.get_settings()[0][line_id]["group_id"]
            line_name = database.get_settings()[0][line_id]["name"]
            group_name = database.get_settings()[0][line_id]["group_name"]
            relay_num = database.get_settings()[0][line_id]["relay_num"]

            last_rule = database.get_last_start_rule(line_id)
            next_rule = database.get_next_active_rule(line_id)
            expected_state = 0

            res[line_id] = {
                "id": line_id,
                "group_id": line_group,
                "line_name": line_name,
                "group_name": group_name,
                "status": status,
                "next_rule": next_rule,
                "last_rule": last_rule,
                "expected_state": expected_state,
                "relay_num": relay_num
            }
        return res
    except Exception as e:
        logging.error(e)
        logging.error("Can't form responce. Exception occured")
        raise e


@app.route("/irrigation_status", methods=["GET"])
def irrigation_status():
    """Return status of raspberry_pi relay."""
    try:
        lines = {}
        for line_id, line in database.get_settings()[0].items():
            if line["line_type"] == "irrigation":
                response_status = remote_controller.line_status(
                    line_id=line_id)
                lines[line_id] = dict(
                    id=line_id, state=int(response_status[line_id]["state"])
                )

        arr = form_responce_for_branches(lines)
        send_branch_status_message(arr)
        return jsonify(branches=arr)
    except Exception as e:
        logging.error(e)
        logging.error("Can't get Raspberri Pi pin status. Exception occured")
        abort(500)


@app.route("/lighting_status", methods=["GET"])
def lighting_status():
    """Return status of lightingn relay."""
    try:
        lines = {}
        for line_id, line in database.get_settings()[0].items():
            if line["line_type"] == "lighting":
                response_status = remote_controller.line_status(
                    line_id=line_id)
                lines[line_id] = dict(
                    id=line_id, state=int(response_status[line_id]["state"])
                )

        arr = form_responce_for_branches(lines)
        send_branch_status_message(arr)
        return jsonify(branches=arr)
    except Exception as e:
        logging.error(e)
        logging.error("Can't get Raspberri Pi pin status. Exception occured")
        abort(500)


@app.route("/linked_device_status", methods=["GET"])
def linked_device_status():
    """Return status of lightingn relay."""
    try:
        lines = {}
        for line_id, line in database.get_settings()[0].items():
            if line["line_type"] == "tank":
                response_status = remote_controller.check_tank_status(
                    line_id=line_id)
                lines[line_id] = dict(
                    id=line_id,
                    device_state=int(response_status[line_id]["device_state"]),
                )

        return jsonify(devices=lines)
    except Exception as e:
        logging.error(e)
        logging.error("Can't get Raspberri Pi pin status. Exception occured")
        abort(500)


@app.route("/tank_status", methods=["GET"])
def tank_status():
    """Return status of lightingn relay."""
    try:
        lines = {}
        for line_id, line in database.get_settings()[0].items():
            if line["line_type"] == "tank":
                response_status = remote_controller.line_status(
                    line_id=line_id)
                lines[line_id] = dict(
                    id=line_id, state=int(response_status[line_id]["state"])
                )

        arr = form_responce_for_branches(lines)
        send_branch_status_message(arr)
        return jsonify(branches=arr)
    except Exception as e:
        logging.error(e)
        logging.error("Can't get Raspberri Pi pin status. Exception occured")
        abort(500)


@app.route("/greenhouse_status", methods=["GET"])
def greenhouse_status():
    """Return status of lightingn relay."""
    try:
        lines = {}
        for line_id, line in database.get_settings()[0].items():
            if line["line_type"] == "greenhouse":
                response_status = remote_controller.line_status(
                    line_id=line_id)
                lines[line_id] = dict(
                    id=line_id, state=int(response_status[line_id]["state"])
                )

        arr = form_responce_for_branches(lines)
        send_branch_status_message(arr)
        return jsonify(branches=arr)
    except Exception as e:
        logging.error(e)
        logging.error("Can't get Raspberri Pi pin status. Exception occured")
        abort(500)


@app.route("/devices/<string:device_id>/", methods=["GET"])
def device_status(device_id):
    """Returns device expected state."""
    LINE_ON = 1
    LINE_OFF = 0

    lines = database.get_device_lines(device_id)
    expected_states = []
    for line in lines:
        _line_id = line[0]
        next_rule = database.get_next_active_rule(_line_id)
        # in case no rule - turn off
        if next_rule is None:
            expected_state = LINE_OFF
        # if there is a rule to stop - device shall be turned on
        elif next_rule['rule_id'] == config.STOP_RULE:
            expected_state = LINE_ON
        # if there is a rule to start - device shall be turned off
        elif next_rule['rule_id'] == config.START_RULE:
            expected_state = LINE_OFF
        else:
            # in any other situation - turn off
            logging.error("Can't predict state")
            expected_state = LINE_OFF

        expected_states.append(dict(
            line_id=database.get_settings()[0][_line_id]['branch_id'],
            relay_num=database.get_settings()[0][_line_id]['relay_num'],
            expected_state=expected_state
        ))

    return jsonify(lines=expected_states)


@app.route("/toogle_line", methods=["GET"])
def toogle_line():
    """Route is used to change branch state to opposite."""
    """Can be executed manually - row will be added to database
    or with rules service - no new row will be added to database"""
    device_id = str(request.args.get("device_id"))
    switch_num = int(request.args.get("switch_num"))

    sql_responce = database.select(
        database.QUERY[mn()].format(device_id, switch_num),
        "fetchall"
    )

    branch_state_avg = 0
    branches = dict()
    for res in sql_responce:
        branch_id = res[0]
        branch = remote_controller.line_status(line_id=branch_id)[branch_id]
        branch_state_avg += branch['state']
        branches[branch_id] = branch

    desired_state = round(branch_state_avg / len(branches))
    desired_state ^= 1

    for res in sql_responce:
        branch_id = res[0]
        if branches[branch_id]['state'] == desired_state:
            continue

        if branches[branch_id]['state'] == 0:
            res_arr = remote_controller.branch_on(line_id=branch_id)
        else:
            res_arr = remote_controller.branch_off(line_id=branch_id)

    send_branch_status_message(res_arr)
    send_history_change_message()

    return jsonify(branches=res_arr)


@app.route("/weather")
@cache.cached(timeout=CACHE_TIMEOUT)
def weather():
    """Blablbal."""
    rain = database.get_rain_volume()

    rain_status = 0
    if rain < config.RAIN_MAX:
        rain_status = 1

    wurl = "http://api.openweathermap.org/data/2.5/weather?id=698782&appid=319f5965937082b5cdd29ac149bfbe9f"
    try:
        response = requests.get(url=wurl)
        response.raise_for_status()
        json_data = json.loads(response.text)
        c_temp = int(json_data["main"]["temp"]) - 273.15
        return jsonify(
            temperature=str(round(c_temp, 2)),
            humidity=str(round(json_data["main"]["humidity"], 2)),
            rain=str(rain),
            rain_status=rain_status,
        )
    except Exception as e:
        logging.error(e)
        logging.error("Can't get weather info Exception occured")
        return jsonify(
            temperature=0, humidity=0, rain=str(rain), rain_status=rain_status
        )


@app.route("/app_settings")
def app_settings():
    """Blablbal."""
    return jsonify(data=database.get_settings()[1])


@app.route("/set_settings", methods=["POST"])
def set_settings():
    """Blablbal."""
    content = request.json["list"]
    database.set_app_settings(content)

    return jsonify(data=database.get_settings()[1])
