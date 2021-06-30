from devices.service_providers.httpx_client import HttpxClient
from devices.models.devices import Message
from fastapi import APIRouter, Depends, status, Response
from fastapi.params import Header
from pydantic import Required

from devices.dependencies import ahttp_client, service_logger
from devices.commands.devices import DeviceCMD

router = APIRouter(prefix="/devices/{device_id}", tags=["registration"])


@router.post(
    "",
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


@router.get(
    "/devices/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def pingalltoregister(
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await cmds.ping_to_register_devices()


@router.get(
    "",
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


@router.post("", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def send_message_to_device(
    device_id: str,
    message: Message,
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
    http_client: HttpxClient = Depends(ahttp_client),
):  
    logger.info(f"Senging message '{message['message']}' to '{device_id}'")
    base_url = cmds.get_device_IP_by_id(device_id)
    response = http_client.post(
        url="http://" + base_url + "/messages", json=message["message"]
    )

    response.raise_for_status()
    response = response.json()
