#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import functools
import logging
import time
import uuid

import requests
import schedule
from astral import LocationInfo
from astral.sun import sun

from scheduler import config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


def get_sunset_time():    
    city = LocationInfo(config.CITY)
    LOGGER.info(
        f"Information for {city.name}/{city.region}\n"
        f"Timezone: {city.timezone}\n"
        f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
    )
    s = sun(city.observer, date=datetime.datetime.now())
    LOGGER.info(
        f'Dawn:    {s["dawn"]}\n'
        f'Sunrise: {s["sunrise"]}\n'
        f'Noon:    {s["noon"]}\n'
        f'Sunset:  {s["sunset"]}\n'
        f'Dusk:    {s["dusk"]}\n'
    )

    return s['sunset']


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        LOGGER.info('Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        LOGGER.info('Job "%s" completed' % func.__name__)
        return result
    return wrapper


@with_logging
def add_rule():
    r = requests.get(
        url=config.BACKEND_IP,
        verify=False,
    )
    r.raise_for_status()

    LINES = r.json()['line_settings']
    LOGGER.info(str(LINES))

    lines_to_fire = []
    for line in LINES.keys():
        if int(line) in config.LINES_TO_ENABLE:
            lines_to_fire.append(
                LINES[line]
            )

    if len(lines_to_fire) == 0:
        LOGGER.warn("No lines to schedule. Aborting")
        return

    LOGGER.info(f"Lines to be scheduled: {lines_to_fire}")

    rules = dict(rules=[])
    messages = []
    start_time = str(
        get_sunset_time() + datetime.timedelta(hours=config.HOURS_AFTER_SUNSET)
    )
    for line in lines_to_fire:
        rules['rules'].append({
            "line_id": int(line["branch_id"]),
            "time": int(line["time"]),
            "intervals": int(line["intervals"]),
            "time_wait": int(line["time_wait"]),
            "repeat_value": 4,  # comes from ongoing rule. equal to ONE TIME
            "date_start": start_time,
            "time_start": start_time,
            "date_time_start": start_time,
            "end_date": start_time,
            "active": 1,
            "rule_id": str(uuid.uuid4()),
            "days": -1,
            "line_name": line["name"],
        })

        messages.append({
            "users": config.USERS,
            "message": f"'{line['name']}' буде включено о {start_time}. Захід сонця: {start_time}"
        })

    LOGGER.info(f"Rules to be planned: {rules}")
    r=requests.post(
        url=config.BACKEND_IP + "/add_ongoing_rule",
        json=rules,
        verify=False,
    )
    r.raise_for_status()

    LOGGER.info(f"Sending messages {messages} to messenger")
    for message in messages:
        r = requests.post(
            config.WEBHOOK_URL_BASE + "/message",
            json=message,
            verify=False,
        )
        r.raise_for_status()


if __name__ == '__main__':
    if len(config.LINES_TO_ENABLE) == 0:
        LOGGER.warn("No lines to schedule set. Please check settings. Aborting")
        exit(1)
    
    schedule.every().day.at(config.TIME_TO_START).do(add_rule)
    while True:
        schedule.run_pending()
        time.sleep(1)
