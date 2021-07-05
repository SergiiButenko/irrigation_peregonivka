from devices.models.sensors import SensorValue
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from typing import Optional

from devices.dependencies import service_logger
from devices.queries.sensors import SensorsNOSQL
from devices.commands.sensors import SensorsCMD

router = APIRouter(
    prefix="/devices/{device_id}/sensors/{sensor_id}",
    tags=["sensors"]
)


@router.get("")
async def get_sensor(
    device_id: str,
    sensor_id: str,
    sensor_sql: SensorsNOSQL = Depends(SensorsNOSQL),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    return await sensor_sql.get_by_id(device_id, sensor_id)


@router.post(
    "/data",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def register(
    device_id: str,
    sensor_id: str,
    sensor_value: SensorValue,
    sensor_cmds: SensorsCMD = Depends(SensorsCMD),
    logger=Depends(service_logger),
):
    """To register sensor values"""
    logger.info(
        f"Register signal from '{device_id}':'{sensor_id}' device_id:sensor_id received.")
    logger.info(f"value: '{sensor_value}'")

    await sensor_cmds.register_sensor_value_by_id(device_id, sensor_id, sensor_value)


@router.get(
    "/data",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def get_value(
    device_id: str,
    sensor_id: str,
    minutes_from_now: int,
    function: Optional[str] = None,
    sorting: Optional[str] = 'ASC',
    sensor_sql: SensorsNOSQL = Depends(SensorsNOSQL),
    logger=Depends(service_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    await sensor_sql.get_values_by_id(
        device_id,
        sensor_id,
        minutes_from_now,
        function,
        sorting
        )
