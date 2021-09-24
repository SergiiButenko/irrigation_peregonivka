import os


class Config:
    PSQL_DATABASE_URI = os.environ['PSQL_DATABASE_URI']
    MONGO_DATABASE_URI = os.environ['MONGO_DATABASE_URI']
    TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
    TELEGRAM_CHAT_ID_COTTAGE = os.environ['TELEGRAM_CHAT_ID_COTTAGE']
    AMQP_URI = os.environ['AMQP_URI']
    DEVICES_URL = os.environ['DEVICES_URL']
    NOTIFY_MIN_BEFORE = 10
