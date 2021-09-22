import os


class Config:
    PSQL_DATABASE_URI = os.environ['PSQL_DATABASE_URI']
    MONGO_DATABASE_URI = os.environ['MONGO_DATABASE_URI']
    TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
    GROUP_CHAT_ID_COTTAGE = os.environ['GROUP_CHAT_ID_COTTAGE']
    AMQP_URI = os.environ['AMQP_URI']