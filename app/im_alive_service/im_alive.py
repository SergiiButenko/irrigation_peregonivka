#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify, request

import eventlet
from flask_socketio import SocketIO

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
    app, async_mode="eventlet", engineio_logger=False, message_queue="redis://"
)


@app.route("/im_alive")
def im_alive():
    """In order to keep device status"""
    device_id = str(request.args.get("device_id"))
    logging.info("Ping signal from '{0}' device id received".format(device_id))
    return jsonify(message="confirmed")
