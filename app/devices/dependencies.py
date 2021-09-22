"""Shared dependencies for the Device Discovety API

The idea is to support callable params for the Depends injections.
"""
from devices.service_providers.device_logger import logger
from devices.service_providers.mongo_db import mongo_db
from devices.service_providers.telegram_bot import telegram_bot
from devices.service_providers.sql_db import psql_db
from databases import Database


from devices.config.config import Config
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.mongo_db import Mongo


def get_sql_db() -> Database:
    return psql_db


def get_config() -> Config:
    return Config


def get_logger():
    return logger


def ahttp_client() -> HttpxClient:
    return HttpxClient


def get_mongo_db() -> Mongo:
    return mongo_db


def get_telegram_bot():
    return telegram_bot
