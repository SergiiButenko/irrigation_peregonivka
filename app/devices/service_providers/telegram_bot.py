import telebot
from devices.config.config import Config

telegram_bot = telebot.TeleBot(Config.TELEGRAM_API_TOKEN)
