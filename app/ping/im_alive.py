#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify, request

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

app = Flask(__name__)

@app.route("/")
def im_alive():
    """In order to keep device status"""
    device_id = str(request.args.get("device_id"))
    logging.info("Ping signal from '{0}' device id received".format(device_id))
    return jsonify(message="confirmed")
