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
import flask
from helpers.common import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


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


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))



if __name__ == '__main__':
    # Start flask server
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=False)
