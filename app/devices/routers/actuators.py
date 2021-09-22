from devices.commands.events import EventsCMD
from devices.queries.devices import DeviceSQL
from devices.schemas.schema import DeviceExpectedState
from fastapi import APIRouter, Depends

from devices.dependencies import get_logger


router = APIRouter(prefix="/devices/{device_id}", tags=["actuator"])


@router.get("/actuators/{actuator_id}", name="Get specific actuator of device")
async def get_actuators(
    device_id: str,
    actuator_id: int,
    device_sql: DeviceSQL = Depends(DeviceSQL),
    logger=Depends(get_logger),
):
    return await device_sql.get_component_by_id(device_id, actuator_id)


@router.get("/actuators/{actuator_id}/state", name="Get state of specific actuator")
async def get_actuator_state(
    device_id: str,
    actuator_id: int,
    device_sql: DeviceSQL = Depends(DeviceSQL),
    logger=Depends(get_logger),
):
    """Change state of actuator."""
    return await device_sql.get_actuator_state(device_id, actuator_id)


@router.put("/actuators/{actuator_id}/state", name="Set state of specific actuator")
async def set_actuator_state(
    device_id: str,
    actuator_id: int,
    state: DeviceExpectedState,
    events_cmds: EventsCMD = Depends(EventsCMD),
    logger=Depends(get_logger),
):
    """Set state of actuator."""
    await events_cmds.try_execute(device_id, actuator_id, "set_state", state)
    return {"message": "Change State event executed"}
