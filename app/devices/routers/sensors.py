from devices.queries.devices import DeviceQRS
from devices.queries.sensors import SensorQRS
from devices.commands.events import EventsCMD
from devices.schemas.schema import SensorValue
from fastapi import APIRouter, Depends

from devices.dependencies import get_current_active_user, get_logger

router = APIRouter(
    prefix="/devices/{device_id}/sensors/{sensor_id}",
    tags=["sensors"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("", name="Get sensor model")
async def get_sensor(
    device_id: str,
    sensor_id: int,
    device_sql: DeviceQRS = Depends(DeviceQRS),
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
    sensor_qrs: SensorQRS = Depends(SensorQRS),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    return await sensor_qrs.get_sensor_values_by_id(
        device_id,
        sensor_id,
        minutes_from_now,
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

    await sensor_qrs.register_sensor_value_by_id(
        device_id,
        sensor_id,
        sensor_value.data
    )

    await events_cmds.try_execute(device_id, sensor_id, 'analyse')

    return {"message": "Data registered"}
