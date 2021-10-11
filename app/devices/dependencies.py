"""Shared dependencies for the Device Discovety API

The idea is to support callable params for the Depends injections.
"""

from devices.routers.helpers.users import get_current_user
from databases import Database
from fastapi import Depends, HTTPException

from devices.config.config import Config
from devices.models.users import User
from devices.service_providers.device_logger import logger
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.mongo_db import Mongo, mongo_db
from devices.service_providers.sql_db import psql_db
from devices.service_providers.telegram_bot import telegram_bot


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_sql_db() -> Database:
    return psql_db


async def get_config() -> Config:
    return Config


async def get_logger():
    return logger


async def ahttp_client() -> HttpxClient:
    return HttpxClient


async def get_mongo_db() -> Mongo:
    return mongo_db


async def get_telegram_bot():
    return telegram_bot
