from devices.models.devices import ActuatorsList
from fastapi import APIRouter, Depends

from devices.dependencies import get_logger

router = APIRouter(
    prefix="/rules",
    tags=["rules"]
)


@router.post("", name="Create set of rules")
async def get_sensor(
    actuators_rules: ActuatorsList,
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Trying to plan '{actuators_rules}'")

    return "OK"
