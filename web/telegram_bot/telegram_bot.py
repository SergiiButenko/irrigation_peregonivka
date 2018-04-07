# -*- coding: utf-8 -*-
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import *
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


def is_api_group(chat_id):
    logging.info("income chat id: {0}; expecting chat id: {1}".format(chat_id, GROUP_CHAT_ID))
    return chat_id == GROUP_CHAT_ID


@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")


@bot.message_handler(commands=['start'])
def on_start(message):
    if not is_api_group(message.chat.id):
        bot.reply_to(message, text_messages['wrong_chat'])
        return

    bot.reply_to(message, text_messages['welcome'])


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    logging.info("ROOT requested")
    return 'OK'


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['info', 'help'])
def on_info(message):
    logging.info(str(message))
    if not is_api_group(message.chat.id):
        bot.reply_to(message, text_messages['wrong_chat'])
        return

    bot.reply_to(message, text_messages['info'])


# # Handle all other messages
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     logging.info(str(message))
#     bot.reply_to(message, message.text)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


@app.route('/notify_users_irrigation_started', methods=['POST'])
def notify_users():
    logging.debug("received request for send_message. post data: {0}".format(request.get_data()))
    data = json.loads(request.get_data().decode())
    users = data['users']
    rule_id = data['rule_id']
    time = data['time']
    timeout = data['timeout']
    user_friendly_name = data['user_friendly_name']

    end_messaging_time = datetime.datetime.strptime(SNOOZE_HOURS['stop_messaging'], '%H:%M').time()
    start_messaging_time = datetime.datetime.strptime(SNOOZE_HOURS['start_messaging'], '%H:%M').time()
    dnow = datetime.datetime.now().time()

    if time_in_range(start_messaging_time, end_messaging_time, dnow):
        logging.info("Snooze hours is on. Message won't be send")
        return json.dumps({'status': 'OK'})
    else:
        logging.info(dnow)
        logging.info(end_messaging_time)
        logging.info(start_messaging_time)
        logging.info(dnow > end_messaging_time)
        logging.info(dnow < start_messaging_time)

    for user in users:
        logging.info("Sending message to {0}. id: {1}".format(user['name'], user['id']))
        # bot.send_message(GROUP_CHAT_ID, "Через {0} хвилин почнеться полив гілки '{1}'. Триватиме {2} хвилин.\nЗайдіть на сайт, щоб відмнінити цей полив".format(timeout, user_friendly_name, time,))  # rule_id))

    logging.info("Done")
    return json.dumps({'status': 'OK'})

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))



if __name__ == '__main__':
    # Start flask server
    logging.info('start')
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=False)
