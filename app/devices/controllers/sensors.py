from devices.models.devices import SensorValue
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from typing import Optional

from devices.dependencies import service_logger
from devices.commands.devices import DeviceCMD

router = APIRouter(
    prefix="/devices/{device_id}/sensors/{sensor_id}",
    tags=["sensors"]
)


@router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def register(
    device_id: str,
    sensor_id: str,
    sensor_value: SensorValue,
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """To register sensor values"""
    logger.info(
        f"Register signal from '{device_id}':'{sensor_id}' device_id:sensor_id received.")
    logger.info(f"value: '{sensor_value}'")

    await cmds.register_sensor_value_by_id(device_id, sensor_id, sensor_value)


@router.get(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def get_value(
    device_id: str,
    sensor_id: str,
    minutes_from_now: int,
    function: Optional[str] = None,
    sorting: Optional[str] = 'ASC',
    cmds: DeviceCMD = Depends(DeviceCMD),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await cmds.get_values_by_id(
        device_id,
        sensor_id,
        minutes_from_now,
        function,
        sorting
        )
