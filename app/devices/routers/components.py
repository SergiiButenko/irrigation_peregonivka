from devices.commands.intervals import IntervalsCMD
from devices.models.users import User
from devices.queries.intervals import IntervalsQRS
from fastapi import APIRouter, Depends
from pydantic.types import StrictStr

from devices.commands.events import EventsCMD
from devices.dependencies import get_current_active_user
from devices.queries.components import ComponentsQRS
from devices.schemas.schema import SensorValue, ComponentExpectedState
from devices.queries.sensors import SensorQRS
from devices.enums.intervals import IntervalPossibleState


router = APIRouter(
    prefix="/components/{component_id}",
    tags=["components"],
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
    current_user: User = Depends(get_current_active_user),
):
    """Get state of component."""
    state = await ComponentsQRS.get_expected_component_state(component_id)
    return {
        'expected_state': state.expected_state,
        'interval': await IntervalsQRS.get_active_interval_by_component_id(component_id, current_user)
    }


@router.put("/state", name="Set state of specific component")
async def set_component_state(
    component_id: str,
    state: ComponentExpectedState,
    current_user: User = Depends(get_current_active_user),
    events_cmds: EventsCMD = Depends(EventsCMD),
):
    """Set state of actuator."""
    if state.current_interval_id is not None:
        await IntervalsCMD.cancel_interval(
            state.current_interval_id,
            IntervalPossibleState.CANCELED,
            current_user
        )

    await events_cmds.try_execute(component_id, "set_state", state.expected_state)
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
