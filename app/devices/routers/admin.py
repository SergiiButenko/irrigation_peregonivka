from fastapi import APIRouter, Depends, status, Response

from devices.dependencies import get_logger
from devices.commands.devices import DeviceCMD

router = APIRouter(
    prefix='/admin',
    tags=["admin_api"]
    )


@router.get(
    "/devices/register",
    name="Reregister all devices IP",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def pingalltoregister(
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await cmds.ping_to_register_devices()


@router.get(
    "/devices/{device_id}/register",
    name="Reregister specific device IP",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def pingsometoregister(
    device_id: str,
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Asking '{device_id}' device id to register.")
    await cmds.ping_to_register_device_by_id(device_id)
