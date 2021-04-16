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
    logging.info(f"Ping signal from '{device_id}' device id received. IP: {request.remote_addr}")
    logging.info(f"Headers: {request.headers}")
    
    return jsonify(message="confirmed")

