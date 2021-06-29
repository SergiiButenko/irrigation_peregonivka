"""Shared dependencies for the Device Discovety API

The idea is to support callable params for the Depends injections.
"""
import logging
from databases import Database

from device_discovery.config.config import Config
from device_discovery.service_providers.httpx_client import HttpxClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

database = Database(Config.DATABASE_URI)


def get_db() -> Database:
    return database


def get_config() -> Config:
    return Config


def service_logger():
    return logging.getLogger("device-discovery")


def ahttp_client() -> HttpxClient:
    return HttpxClient
