# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import inspect
import os
from config.config import *
import telebot
import logging
import json
from flask import Flask
from flask import request
from flask import abort
import requests
from helpers.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)


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
        bot.send_message(user['id'], str(message))

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
        bot.send_message(GROUP_CHAT_ID, "Через {0} хвилин почнеться полив гілки '{1}'. Триватиме {2} хвилин.\nЗайдіть на сайт, щоб відмнінити цей полив".format(timeout, user_friendly_name, time,))  # rule_id))

    logging.info("Done")
    return json.dumps({'status': 'OK'})


if __name__ == '__main__':
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()

    # Set webhook
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    # Start flask server
    logging.info('start')
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=False)
