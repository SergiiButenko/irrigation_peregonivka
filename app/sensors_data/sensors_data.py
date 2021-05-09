#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify, request
from mongo_db.mongo_db import Mongo

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

app = Flask(__name__)
MongoDatabase = Mongo()


@app.route("/devices/<string:device_id>/sensors/<string:sensor_id>", methods=["POST"])
def register_sensor_value(device_id, sensor_id):
    logging.info(f"Registering data in database. {device_id}:{sensor_id}")
    data = request.json
    MongoDatabase.register_sensor_data(sensor_id, data)

    return dict(data=data), 201


@app.route("/devices/<string:device_id>/sensors/<string:sensor_id>", methods=["GET"])
def get_sensor_value(device_id, sensor_id):
    data = MongoDatabase.get_latest_sensor_data(sensor_id)
    return dict(data=data)
