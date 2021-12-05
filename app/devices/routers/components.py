from devices.clients.notification_service import NotificationServiceClient
from fastapi import APIRouter, Depends
from pydantic.types import StrictStr

from devices.commands.components import ComponentsCMD
from devices.commands.events import EventsCMD
from devices.dependencies import get_current_active_user, get_notification_service
from devices.models.users import User
from devices.queries.components import ComponentsQRS
from devices.queries.sensors import SensorQRS
from devices.schemas.schema import ComponentExpectedState, SensorValue

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
    return await ComponentsCMD.get_component_state(component_id, current_user)


@router.put("/state", name="Set state of specific component")
async def set_component_state(
    component_id: str,
    state: ComponentExpectedState,
    events_cmds: EventsCMD = Depends(EventsCMD),
    current_user: User = Depends(get_current_active_user),
):
    """Set state of actuator."""
    await events_cmds.try_execute(
        component_id, "set_state", state.expected_state, current_user
    )
    return {"message": "Change State event executed"}


@router.get("/data", name="Get sensor data")
async def get_value(
    component_id: str,
    limit: int = 10,
    sensor_qrs: SensorQRS = Depends(SensorQRS),
):
    """In order to keep device status"""
    return await ComponentsCMD.get_component_data(component_id, limit=limit)


@router.post("/data", name="Register sensor data")
async def register_value(
    component_id: StrictStr,
    sensor_value: SensorValue,
    events_cmds: EventsCMD = Depends(EventsCMD),
    notification_service: NotificationServiceClient = Depends(get_notification_service)
):
    """To register sensor values"""
    return await ComponentsCMD.register_component_data(component_id, sensor_value, events_cmds, notification_service)
