from fastapi import FastAPI

from devices.dependencies import database
from devices.controllers import (
    device_registration,
    actuators,
    sensors
)

app = FastAPI(
    title="Irrigation Device Discovery API",
    description="The Device Discovery API register and renew IP of devices.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(device_registration.router)
app.include_router(actuators.router)
app.include_router(sensors.router)
