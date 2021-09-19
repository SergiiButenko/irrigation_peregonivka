"""Shared dependencies for the Device Discovety API

The idea is to support callable params for the Depends injections.
"""
import logging
from databases import Database
from motor.motor_asyncio import AsyncIOMotorClient

from devices.config.config import Config
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.mongo_db import Mongo

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

_psql_db = Database(Config.PSQL_DATABASE_URI)
_mongo_db = AsyncIOMotorClient(Config.MONGO_DATABASE_URI)


def psql_db() -> Database:
    return _psql_db


def get_config() -> Config:
    return Config


def get_logger():
    return logging.getLogger("devices")


def ahttp_client() -> HttpxClient:
    return HttpxClient


def mongo_db() -> Mongo:
    return Mongo(_mongo_db, get_logger())
