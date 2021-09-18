from devices.queries.devices import DeviceSQL
from devices.queries.sensors import SensorQRS
from devices.commands.events import EventsCMD
from devices.models.devices import SensorValue
from fastapi import APIRouter, Depends
from typing import Optional

from devices.dependencies import get_logger

router = APIRouter(
    prefix="/devices/{device_id}/sensors/{sensor_id}",
    tags=["sensors"]
)


@router.get("", name="Get sensor model")
async def get_sensor(
    device_id: str,
    sensor_id: int,
    device_sql: DeviceSQL = Depends(DeviceSQL),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info("Asking all devices to register.")
    return await device_sql.get_component_by_id(device_id, sensor_id)


@router.get(
    "/data",
    name="Get sensor data"
)
async def get_value(
    device_id: str,
    sensor_id: int,
    minutes_from_now: int,
    function: Optional[str] = None,
    sorting: Optional[str] = 'ASC',
    sensor_qrs: SensorQRS = Depends(SensorQRS),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    return await sensor_qrs.get_sensor_values_by_id(
        device_id,
        sensor_id,
        minutes_from_now,
        function,
        sorting
        )


@router.post(
    "/data",
    name="Register sensor data"
)
async def register(
    device_id: str,
    sensor_id: int,
    sensor_value: SensorValue,
    events_cmds: EventsCMD = Depends(EventsCMD),
    sensor_qrs: SensorQRS = Depends(SensorQRS),
    logger=Depends(get_logger),
):
    """To register sensor values"""
    logger.info(
        f"Register signal from '{device_id}':'{sensor_id}' \
        device_id:sensor_id received."
    )
    logger.info(f"value: '{sensor_value}'")

    await sensor_qrs.register_sensor_value_by_id(
        device_id,
        sensor_id,
        sensor_value.data
    )

    await events_cmds.try_execute(device_id, sensor_id, 'analyse')

    return {"message": "Data registered"}
