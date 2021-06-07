#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

app = FastAPI()


@app.route("/")
def device_discovery():
    """In order to keep device status"""
    device_id = str(request.args.get("device_id"))
    logging.info(f"Ping signal from '{device_id}' device id received.")

    device_ip = request.headers.get('X-Real-IP')
    logging.info(f"device_ip: {device_ip}")

    logging.debug(f"Headers: {request.headers}")

    if device_ip is None:
        logging.warning(f"No IP in headers. Cannot register IP in database for {device_id}")
        return jsonify(message="No IP in headers. rejected"), 400

    logging.info(f"Registering IP in database. {device_id}:{device_ip}")
    database.set_device_ip(device_id, device_ip)
    return jsonify(message="confirmed")
