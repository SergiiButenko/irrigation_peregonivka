from devices.queries.actuators import ActuatorsSQL
from devices.models.actuators import State
from fastapi import APIRouter, Depends

from devices.dependencies import service_logger
from devices.commands.actuators import ActuatorCMD


router = APIRouter(
    prefix="/devices/{device_id}",
    tags=["actuator"]
)


@router.get(
    "/actuators/{actuator_id}",
    name="Get specific actuator of device"
)
async def get_actuators(
    device_id: str,
    actuator_id: int,
    actuators_sql: ActuatorsSQL = Depends(ActuatorsSQL),
    logger=Depends(service_logger),
):
    """Change state of actuator."""
    return actuators_sql.get_by_id(device_id, actuator_id)


@router.get(
    "/actuators/{actuator_id}/state",
    name="Get state of specific actuator"
)
async def get_actuator_state(
    device_id: str,
    actuator_id: str,
    state: State,
    actuators_cmds: ActuatorCMD = Depends(ActuatorCMD),
    logger=Depends(service_logger),
):
    """Change state of actuator."""
    return actuators_cmds.get_actuator_state(device_id, actuator_id, state)


@router.put(
    "/actuators/{actuator_id}/state",
    name="Set state of specific actuator"
)
async def set_actuator_state(
    device_id: str,
    actuator_id: str,
    state: State,
    actuators_cmds: ActuatorCMD = Depends(ActuatorCMD),
    logger=Depends(service_logger),
):
    """Set state of actuator."""
    actuators_cmds.set_actuator_state(device_id, actuator_id, state)
