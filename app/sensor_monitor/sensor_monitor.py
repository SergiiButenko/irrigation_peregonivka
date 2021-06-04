#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from flask import Flask, request, jsonify
from mongo_db.mongo_db import Mongo
from sensors_monitor import config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

app = Flask(__name__)
MongoDatabase = Mongo(config.MONGO_URI)


@app.route("/devices/<string:device_id>/sensors/<string:sensor_id>", methods=["POST"])
def register_sensor_value(device_id, sensor_id):
    logging.info(f"Registering data in database. {device_id}:{sensor_id}")
    data = request.json
    MongoDatabase.register_sensor_data(sensor_id, data)

    return dict(data=data)


@app.route("/devices/<string:device_id>/sensors/<string:sensor_id>", methods=["GET"])
def get_sensor_value(device_id, sensor_id):
    data = MongoDatabase.get_latest_sensor_data(sensor_id)
    
    return jsonify(data=data)



@app.route("/stop_filling")
def stop_filling():
    """Blablbal."""

    device_id = "upper_tank"
    line_id = config.LINES_UPPER_TANK.get(device_id, None)

    logging.info(
        "INERUPT SIGNAL RESEIVED FROM '{0}' device!".format(device_id))
    database.update(database.QUERY[mn()])

    if line_id is None:
        logging.error("Unsupported '{0}' device id!".format(device_id))
        return json.dumps({"status": "Unsupported '{0}' device id!".format(device_id)})

    _no_key = False
    response_arr = remote_controller.line_status(line_id=line_id)
    if response_arr[line_id]["state"] == 0:
        logging.info(
            "Line '{0}' is not active. Message won't be send.".format(line_id))
        return json.dumps(
            {
                "status": "Line '{0}' is not active. Message won't be send.".format(
                    line_id
                )
            }
        )

    last_time_sent = redis_provider.get_time_last_notification(
        key=config.REDIS_KEY_FOR_UPPER_TANK)
    if last_time_sent is None:
        redis_provider.set_time_last_notification(date=datetime.datetime.now())
        last_time_sent = redis_provider.get_time_last_notification(
            key=config.REDIS_KEY_FOR_UPPER_TANK)
        _no_key = True

    delta = datetime.datetime.now() - last_time_sent
    if delta.seconds > 60 * config.TANK_NOTIFICATION_MINUTES or _no_key is True:
        try:
            logging.info("Deactivating line '{0}'.".format(line_id))
            deactivate_branch(line_id=line_id, mode="manually")
            logging.info("Line deactivated")
            message = "Водопостачання вимкнено автоматично."
        except Exception as e:
            logging.error(e)
            logging.error(
                "Can't deactivate line '{0}'. Ecxeption occured".format(
                    line_id)
            )
            message = "Помилка. Водопостачання не вимкнено!"

        try:
            _users_list = config.TELEGRAM_USERS[device_id]
            logging.info(
                "Sending notify_filled message to users: '{0}'.".format(
                    str(_users_list)
                )
            )
            payload = {"users": _users_list}
            response = requests.post(
                config.WEBHOOK_URL_BASE + "/notify_filled",
                json=payload,
                verify=False,
            )
            response.raise_for_status()
            logging.info("Messages send.")
        except Exception as e:
            logging.error(e)
            logging.error("Can't send rule to telegram. Ecxeption occured")

        try:

            logging.info("Updating redis.")
            redis_provider.set_time_last_notification(
                date=datetime.datetime.now())
            logging.info("Redis updated")
        except Exception as e:
            logging.error(e)
            logging.error("Can't update redis. Exception occured")

        try:
            logging.info(
                "Sending line deactivated message to users: '{0}'.".format(
                    str(_users_list)
                )
            )
            payload = {"users": _users_list, "message": message}
            response = requests.post(
                config.WEBHOOK_URL_BASE + "/message",
                json=payload,
                verify=False,
            )
            response.raise_for_status()
            logging.info("Messages send.")
        except Exception as e:
            logging.error(e)
            logging.error("Can't send rule to telegram. Exception occured")
            return json.dumps(
                {"status": "Can't send rule to telegram. Exception occured"}
            )

        return json.dumps({"status": "Redis updated"})
    else:
        logging.info(
            "{0} minutes not passed yet. Send message pending.".format(
                config.TANK_NOTIFICATION_MINUTES
            )
        )
        return json.dumps(
            {
                "status": "{0} minutes not passed yet. Send message pending.".format(
                    config.TANK_NOTIFICATION_MINUTES
                )
            }
        )


@app.route("/cesspool")
def cesspool():
    """Blablbal."""

    logging.info("CESSPOOL SIGNAL RESEIVED")

    device_id = "cesspool"
    _no_key = False

    last_time_sent = redis_provider.get_time_last_notification(
        key=config.REDIS_KEY_FOR_CESSTOOL)
    if last_time_sent is None:
        redis_provider.set_time_last_notification(
            date=datetime.datetime.now(), key=config.REDIS_KEY_FOR_CESSTOOL
        )
        last_time_sent = redis_provider.get_time_last_notification(
            key=config.REDIS_KEY_FOR_CESSTOOL)
        _no_key = True

    delta = datetime.datetime.now() - last_time_sent
    if delta.seconds > 60 * config.CESSTOOL_NOTIFICATION_MINUTES or _no_key is True:
        message = "Рівень води в септику вище норми."

        try:

            logging.info("Updating redis.")
            redis_provider.set_time_last_notification(
                date=datetime.datetime.now(), key=config.REDIS_KEY_FOR_CESSTOOL
            )
            logging.info("Redis updated")
        except Exception as e:
            logging.error(e)
            logging.error("Can't update redis. Exception occured")

        try:
            _users_list = config.TELEGRAM_USERS[device_id]
            logging.info(
                "Sending warning message to users: '{0}'.".format(
                    str(_users_list))
            )
            payload = {"users": _users_list, "message": message}
            response = requests.post(
                config.WEBHOOK_URL_BASE + "/message",
                json=payload,
                verify=False,
            )
            response.raise_for_status()
            logging.info("Messages send.")
        except Exception as e:
            logging.error(e)
            logging.error("Can't send rule to telegram. Ecxeption occured")
            return json.dumps(
                {"status": "Can't send rule to telegram. Exception occured"}
            )

        return json.dumps({"status": "Redis updated"})
    else:
        logging.info(
            "{0} minutes not passed yet. Send message pending.".format(
                config.CESSTOOL_NOTIFICATION_MINUTES
            )
        )
        return json.dumps(
            {
                "status": "{0} minutes not passed yet. Send message pending.".format(
                    config.CESSTOOL_NOTIFICATION_MINUTES
                )
            }
        )

@app.route("/weather_station")
def weather_station():
    api_key = str(request.args.get("api_key"))
    device_shotname = str(request.args.get("device_shotname"))
    device_id = str(request.args.get("device_id"))
    rel_pressure_rounded = str(request.args.get("rel_pressure_rounded"))
    measured_temp = str(request.args.get("measured_temp"))
    measured_humi = str(request.args.get("measured_humi"))
    volt = str(request.args.get("volt"))
    measured_pres = str(request.args.get("measured_pres"))
    DewpointTemperature = str(request.args.get("DewpointTemperature"))
    HeatIndex = str(request.args.get("HeatIndex"))
    status = str(request.args.get("status"))

    logging.info(f"""
    weather_station signal from '{device_id}' device id received;
    api_key = {api_key}
    device_shotname = {device_shotname}
    device_id = {device_id}
    rel_pressure_rounded = {rel_pressure_rounded}
    measured_temp = {measured_temp}
    measured_humi = {measured_humi}
    volt = {volt}
    measured_pres = {measured_pres}
    DewpointTemperature = {DewpointTemperature}
    HeatIndex = {HeatIndex}
    status = {status}
    """)
    return jsonify(message="confirmed")

    if (
        database.insert_weather(
            sensor_shortname=device_id, temp=temp, hum=hum, press=press, voltage=voltage
        )
        is True
    ):
        logging.info("Info registered in database.")
    else:
        logging.error("Error while insert occured. ")
