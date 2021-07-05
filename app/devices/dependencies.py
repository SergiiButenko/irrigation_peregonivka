"""Shared dependencies for the Device Discovety API

The idea is to support callable params for the Depends injections.
"""
import logging
from databases import Database

from devices.config.config import Config
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.mongo_db import Mongo

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

database = Database(Config.PSQL_DATABASE_URI)


def get_db() -> Database:
    return database


def get_config() -> Config:
    return Config


def service_logger():
    return logging.getLogger("devices")


def ahttp_client() -> HttpxClient:
    return HttpxClient


def mongo_db() -> Mongo:
    return Mongo(Config.MONGO_DATABASE_URI)
