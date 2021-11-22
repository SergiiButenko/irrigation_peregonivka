from fastapi import APIRouter, Depends
from pydantic.types import StrictStr, UUID4

from devices.commands.events import EventsCMD
from devices.dependencies import get_current_active_user
from devices.queries.components import ComponentsQRS
from devices.schemas.schema import ComponentExpectedState, SensorValue
from devices.queries.sensors import SensorQRS


router = APIRouter(
    prefix="/components/{component_id}",
    tags=["actuator"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("", name="Get specific component of device")
async def get_components(
    component_id: str,
    ComponentsQRS: ComponentsQRS = Depends(ComponentsQRS),
):
    component = await ComponentsQRS.get_component_by_id(component_id)

    return component


@router.get("/state", name="Get state of specific component")
async def get_component_state(
    component_id: str,
    ComponentsQRS: ComponentsQRS = Depends(ComponentsQRS),
):
    """Change state of actuator."""
    return await ComponentsQRS.get_expected_component_state(component_id)


@router.put("/state", name="Set state of specific component")
async def set_component_state(
    component_id: str,
    state: ComponentExpectedState,
    events_cmds: EventsCMD = Depends(EventsCMD),
):
    """Set state of actuator."""
    await events_cmds.try_execute(component_id, "set_state", state)
    return {"message": "Change State event executed"}


@router.get("/data", name="Get sensor data")
async def get_value(
    component_id: str,
    minutes_from_now: int,
    sensor_qrs: SensorQRS = Depends(SensorQRS),
):
    """In order to keep device status"""
    return await sensor_qrs.get_sensor_values_by_id(
        component_id,
        minutes_from_now,
    )


@router.post("/data", name="Register sensor data")
async def register_value(
    component_id: StrictStr,
    sensor_value: SensorValue,
    events_cmds: EventsCMD = Depends(EventsCMD),
    sensor_qrs: SensorQRS = Depends(SensorQRS),
):
    """To register sensor values"""
    await sensor_qrs.register_sensor_value_by_id(
        component_id, sensor_value.data
    )
    await events_cmds.try_execute(component_id, "analyse")
    return {"message": "Data registered"}
