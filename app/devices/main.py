from devices.commands.rules import RulesCMD
from fastapi import FastAPI

from devices.service_providers.sql_db import psql_db
from devices.routers import (
    devices,
    actuators,
    sensors,
    telegram,
    rules,
    auth,
    websockets,
    groups
)
from devices.service_providers.device_logger import logger
from devices.service_providers.celery import celery_app

app = FastAPI(
    title="Irrigation Device Discovery API",
    description="The Device Discovery API register and renew IP of devices.",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    logger.info("Deleting queued messaged")
    celery_app.control.purge()
    await psql_db.connect()
    logger.info("Analysing rules to enqueu")
    await RulesCMD.analyse_and_enqueue()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Deleting queued messaged")
    celery_app.control.purge()
    await psql_db.disconnect()


app.include_router(devices.router)
app.include_router(actuators.router)
app.include_router(sensors.router)
app.include_router(telegram.router)
app.include_router(rules.router)
app.include_router(auth.router)
app.include_router(websockets.router)
app.include_router(groups.router)

