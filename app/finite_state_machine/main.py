from fastapi import FastAPI, Header, Depends, status
from fastapi.responses import Response
from pydantic import Required

from device_discovery.dependencies import database, service_logger
from device_discovery.commands.devices import DeviceCMD

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


@app.post(
    "/devices/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def register(
    device_id: str,
    X_Real_IP: str = Header(Required),
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """In order to keep device ip"""
    logger.info(f"Register signal from '{device_id}' device id received.")

    await cmds.register_device_by_id(device_id, X_Real_IP)
    logger.info(f"device_ip register: {X_Real_IP} for {device_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/devices/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def pingalltoregister(
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await cmds.ping_to_register_devices()


@app.get(
    "/devices/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def pingsometoregister(
    device_id: str,
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info(f"Asking '{device_id}' device id to register.")
    await cmds.ping_to_register_device_by_id(device_id)
