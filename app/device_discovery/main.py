from fastapi import FastAPI, Header, Depends, status
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


@app.post("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def register(
    device_id: str,
    X_Real_IP: str = Header(Required),
    cmd: DeviceCMD.register_device_by_id = Depends(),
    logger=Depends(service_logger),
):
    """In order to keep device ip"""
    logger.info(f"Register signal from '{device_id}' device id received.")

    cmd(device_id, X_Real_IP)
    logger.info(f"device_ip register: {X_Real_IP} for {device_id}")


@app.get("/devices/", status_code=status.HTTP_204_NO_CONTENT)
async def pingalltoregister(
    cmd: DeviceCMD.ping_to_register_devices = Depends(),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await cmd()


@app.get("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def pingsometoregister(
    device_id: str,
    cmd: DeviceCMD.ping_to_register_device_by_id = Depends(),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info(f"Asking '{device_id}' device id to register.")
    await cmd(device_id)


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=5000)
