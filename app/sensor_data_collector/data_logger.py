import logging
import os

import requests
import datetime
import time

import sqlite_database as database
from helpers import mn
from backend import remote_controller


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

SENSORS = {}
LINES = {}


def setup_sensors_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        logging.info(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            SENSORS[key] = {"id": row[0], "type": row[1], "base_url": row[2]}

        logging.info(SENSORS)
    except Exception as e:
        logging.error(
            "Exceprion occured when trying to get settings for all sensors. {0}".format(
                e
            )
        )


def setup_lines_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            LINES[key] = {"id": row[0], "moisture_id": row[1]}

        logging.info(LINES)
    except Exception as e:
        logging.error(
            "Exceprion occured when trying to get settings for all branches. {0}".format(
                e
            )
        )


def inverse(val):
    logging.info("   not inversed value {0}".format(val))
    return round(100 - val, 2)


def temp_sensors():
    logging.info("Getting temperature:")
    now = datetime.datetime.now()
    for sensor_id, sensor in SENSORS.items():
        if sensor["type"] == "air_sensor":
            response = remote_controller.air_sensor(sensor_id)
            logging.info("Air temp: {0}".format(str(response)))
            database.update(
                database.QUERY[mn() + "_air"].format(
                    response[sensor_id]["id"],
                    response[sensor_id]["air_temp"],
                    response[sensor_id]["air_hum"],
                    now.strftime("%Y-%m-%d %H:%M"),
                )
            )
        elif sensor["type"] == "ground_sensor":
            response = remote_controller.ground_sensor(sensor_id)
            while response[sensor_id]["ground_temp"] == 85.00:
                logging.info("Sensor send basic temp. Retry.")
                response = remote_controller.ground_sensor(sensor_id)

            logging.info("Ground temp: {0}".format(str(response)))
            database.update(
                database.QUERY[mn() + "_ground"].format(
                    response[sensor_id]["id"],
                    response[sensor_id]["ground_temp"],
                    now.strftime("%Y-%m-%d %H:%M"),
                )
            )


def migrate_data():
    database.select(database.QUERY[mn()])

    database.update(database.QUERY[mn() + "_insert"])


if __name__ == "__main__":
    while 1:
        logging.info("Start")
        setup_sensors_datalogger()
        setup_lines_datalogger()
        remote_controller.init_remote_lines()
        temp_sensors()
        logging.info("Done!")
        time.sleep(int(os.environ["RESTART_INTERVAL_MIN"]) * 60)
