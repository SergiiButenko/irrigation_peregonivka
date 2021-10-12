from devices.schemas.schema import Message
from fastapi import APIRouter, Depends, status, Response
from fastapi.params import Header
from pydantic import Required

from devices.dependencies import get_current_active_user, get_logger
from devices.commands.devices import DeviceCMD

router = APIRouter(
    prefix="/devices/{device_id}",
    tags=["registration"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post(
    "/register",
    name="Device IP registration",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def register(
    device_id: str,
    X_Real_IP: str = Header(Required),
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(get_logger),
):
    """In order to keep device ip"""
    logger.info(f"Register signal from '{device_id}' device id received.")

    await cmds.register_device_by_id(device_id, X_Real_IP)
    logger.info(f"device_ip register: {X_Real_IP} for {device_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/message",
    name="Send message to device",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def send_message_to_device(
    device_id: str,
    message: Message,
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(get_logger),
):
    logger.info(f"Senging message '{message['message']}' to '{device_id}'")
    await cmds.send_message_to_device(message=message["message"])
