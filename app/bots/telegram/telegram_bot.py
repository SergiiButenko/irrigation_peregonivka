# -*- coding: utf-8 -*-
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
twoup = os.path.dirname(parentdir)
sys.path.insert(0, twoup)


import inspect
import os
import time
from config.config import *
import telebot
import logging
import json
from flask import Flask
from flask import request
from flask import abort
import requests
from common.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


bot = telebot.TeleBot(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

app = Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'OK'


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@app.route('/notify_filled', methods=['POST'])
def notify_filled():
    logging.info("received request for notify_filled. post data: {0}".format(request.get_data()))
    data = json.loads(request.get_data().decode())
    users = data['users']

    for user in users:
        logging.info("Sending message to {0}. id: {1}".format(user['name'], user['id']))
        bot.send_message(user['id'], "Верхня бочка заповнена. Вимкніть водопостачання.")

    logging.info("Done")
    return json.dumps({'status': 'OK'})


@app.route('/send_message', methods=['POST'])
def send_message():
    logging.info("received request for send message. post data: {0}".format(request.get_data()))
    data = json.loads(request.get_data().decode())
    users = data.get('users')
    message = data.get('message')

    for user in users:
        logging.info("Sending message '{0}'' to {1}. id: {2}".format(str(message), user['name'], user['id']))
        res = bot.send_message(user['id'], str(message))
        logging.debug("Responce: {0}".format(str(res)))

    logging.info("Done")
    return json.dumps({'status': 'OK'})


@app.route('/notify_users_irrigation_started', methods=['POST'])
def notify_users():
    logging.debug("received request for send_message. post data: {0}".format(request.get_data()))
    data = json.loads(request.get_data().decode())
    users = data['users']
    time = data['time']
    timeout = data['timeout']
    user_friendly_name = data['user_friendly_name']

    for user in users:
        logging.info("Sending message to {0}. id: {1}".format(user['name'], user['id']))
        res = bot.send_message(user['id'], "Через {0} хвилин почнеться полив гілки '{1}'. Триватиме {2} хвилин.".format(timeout, user_friendly_name, time))
        logging.debug("Responce: {0}".format(str(res)))

    logging.info("Done")
    return json.dumps({'status': 'OK'})


# Start flask server
logging.info('start')
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(0.1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
time.sleep(0.1)
