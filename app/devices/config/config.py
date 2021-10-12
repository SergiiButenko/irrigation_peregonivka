import os


class Config:
    PSQL_DATABASE_URI = os.environ['PSQL_DATABASE_URI']
    MONGO_DATABASE_URI = os.environ['MONGO_DATABASE_URI']
    TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
    TELEGRAM_CHAT_ID_COTTAGE = os.environ['TELEGRAM_CHAT_ID_COTTAGE']
    AMQP_URI = os.environ['AMQP_URI']
    DEVICES_URL = os.environ['DEVICES_URL']
    SERVICE_USERNAME = os.environ['SERVICE_USERNAME']
    SERVICE_PASSWORD = os.environ['SERVICE_PASSWORD']
    NOTIFY_MIN_BEFORE = 10
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SECRET_KEY = "026d5c7735ae575d5a3e7a45ecea184140df573ea70fed22e8d4a3a1e9cd0020"
    ALGORITHM = "HS256"
