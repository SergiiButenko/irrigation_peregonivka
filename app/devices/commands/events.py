from devices.schemas.schema import DeviceExpectedState
from fastapi import BackgroundTasks
from devices.libraries.events_library.event_factory import EventFactory
from devices.commands.devices import DeviceCMD


class EventsCMD:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
    ):
        self.background_tasks = background_tasks

    async def try_execute(self, device_id: str, component_id: int, in_event: str, state: DeviceExpectedState) -> None:
        device = await DeviceCMD.get_device_by_id(device_id)
        event = EventFactory.get(device, component_id, in_event)
        self.background_tasks.add_task(
            event,
            device,
            component_id,
            state,
        )
