#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import logging
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter

import requests
from flask import Flask, render_template, request
from flask_caching import Cache

import sqlite_database as database
from irrigation_helpers import convert_to_datetime, mn, form_date_description, date_handler

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "simple"})

CACHE_TIMEOUT = 600

BRANCHES_SETTINGS = {}


@app.route("/pumps")
@cache.cached(timeout=CACHE_TIMEOUT)
def pumps():
    """Index page."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item["line_type"] == "irrigation" and item["is_pump"] == 1:
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "group_id": item["group_id"],
                    "group_name": item["group_name"],
                    "is_pump": item["is_pump"],
                    "name": item["name"],
                    "default_time": item["time"],
                    "default_interval": item["intervals"],
                    "default_time_wait": item["time_wait"],
                    "start_time": item["start_time"],
                }
            )

    branch_list.sort(key=itemgetter("group_name"))
    grouped = {}
    for key, group in groupby(branch_list, itemgetter("group_name")):
        grouped[key] = list([thing for thing in group])

    return render_template("pumps.html", my_list=grouped)


@app.route("/greenhouse")
@cache.cached(timeout=CACHE_TIMEOUT)
def greenhouse():
    """Index page."""
    my_list = {}
    my_list["sensors"] = database.get_temperature()

    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item["line_type"] == "greenhouse":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "group_id": item["group_id"],
                    "group_name": item["group_name"],
                    "is_pump": item["is_pump"],
                    "name": item["name"],
                    "default_time": item["time"],
                    "default_interval": item["intervals"],
                    "default_time_wait": item["time_wait"],
                    "start_time": item["start_time"],
                }
            )

    branch_list.sort(key=itemgetter("id"))
    my_list["lines"] = branch_list
    my_list["temperature"] = database.get_temperature2()

    return render_template("greenhouse.html", my_list=my_list)


@app.route("/tank")
@cache.cached(timeout=CACHE_TIMEOUT)
def tank():
    """Return branch names."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item["line_type"] == "tank":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                }
            )

    return render_template("tank.html", my_list=branch_list)


@app.route("/lighting")
@cache.cached(timeout=CACHE_TIMEOUT)
def lighting():
    """Return branch names."""
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item["line_type"] == "lighting":
            branch_list.append(
                {
                    "id": item["branch_id"],
                    "name": item["name"],
                    "default_time": item["time"],
                    "group_id": item["group_id"],
                    "group_name": item["group_name"],
                }
            )

    branch_list.sort(key=itemgetter("group_id"))
    grouped = {}
    for key, group in groupby(branch_list, itemgetter("group_id")):
        grouped[key] = list([thing for thing in group])

    return render_template("lighting.html", my_list=grouped)


@app.route("/add_rule")
def add_rule_page():
    if "add_to_date" in request.args:
        days = int(request.args.get("add_to_date"))

    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if (
            item is not None
            and item["line_type"] == "irrigation"
            and item["is_pump"] == 0
        ):
            start_time = convert_to_datetime(item["start_time"])
            branch_list.append(
                {
                    "line_id": item["branch_id"],
                    "line_name": item["name"],
                    "default_time": item["time"],
                    "default_interval": item["intervals"],
                    "default_time_wait": item["time_wait"],
                    "start_time": (
                        "%s:%s" % (start_time.strftime("%H"), start_time.strftime("%M"))
                    ),
                    "start_date": str(
                        datetime.date.today() + datetime.timedelta(days=days)
                    ),
                }
            )

    """Add rule page."""
    return render_template("add_rule.html", my_list=branch_list)


@app.route("/history")
def history():
    """Return history page if no parameters passed and only table body if opposite."""
    if "days" in request.args:
        days = int(request.args.get("days"))
    else:
        days = 7

    # SELECT l.interval_id, li.name, l.date, l.timer as \"[timestamp]\", l.active, l.time
    grouped_rules = OrderedDict()
    list_arr = database.select(database.QUERY[mn()].format(days), "fetchall")
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
                time_wait = int(
                    (intervals[1][3] - intervals[0][3]).total_seconds() / 60
                    - intervals[0][5]
                )

            row = intervals[0]
            rules.append(
                dict(
                    line_name=row[1],
                    date=row[2].strftime("%m/%d/%Y"),
                    date_description=form_date_description(row[2]),
                    timer=date_handler(row[3]),
                    ative=row[4],
                    time=row[5],
                    intervals=intervals_quantity,
                    interval_id=row[0],
                    time_wait=time_wait,
                )
            )

        rules.sort(key=itemgetter("date"))
        for key, group in groupby(rules, itemgetter("date")):
            grouped_rules[key] = [thing for thing in group]

        for key, value in grouped_rules.items():
            value.sort(key=itemgetter("timer"))

    return render_template("history.html", my_list=grouped_rules)


@app.route("/")
def planner():
    branch_list = []
    for item_id, item in BRANCHES_SETTINGS.items():
        if item["line_type"] == "irrigation" and item["is_pump"] == 0:
            branch_list.append(
                {
                    "line_id": item["branch_id"],
                    "group_id": item["group_id"],
                    "group_name": item["group_name"],
                    "is_pump": item["is_pump"],
                    "line_name": item["name"],
                    "default_time": item["time"],
                    "default_interval": item["intervals"],
                    "default_time_wait": item["time_wait"],
                    "start_time": item["start_time"],
                }
            )

    branch_list.sort(key=itemgetter("group_id"))
    grouped = {}
    for key, group in groupby(branch_list, itemgetter("group_id")):
        grouped[key] = list([thing for thing in group])

    return render_template("planner.html", my_list=grouped)


logging.info("Get app settings")
BRANCHES_SETTINGS = database.get_settings()[0]

logging.info("Staring app")
