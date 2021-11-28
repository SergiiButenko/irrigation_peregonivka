import telebot
from notification_service.config.config import Config

telegram_bot = telebot.TeleBot(Config.TELEGRAM_API_TOKEN)
