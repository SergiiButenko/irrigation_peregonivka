from fastapi import FastAPI

from devices.service_providers.sql_db import psql_db
from devices.routers import (
    devices,
    actuators,
    sensors,
    telegram,
    rules
)

app = FastAPI(
    title="Irrigation Device Discovery API",
    description="The Device Discovery API register and renew IP of devices.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await psql_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await psql_db.disconnect()


app.include_router(devices.router)
app.include_router(actuators.router)
app.include_router(sensors.router)
app.include_router(telegram.router)
app.include_router(rules.router)
