from fastapi import BackgroundTasks
from devices.libraries.events_library.event_factory import EventFactory
from devices.commands.devices import DeviceCMD


class EventsCMD:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
    ):
        self.background_tasks = background_tasks

    async def try_execute(self, component_id: str, in_event: str, *args, **kwargs) -> None:
        device = await DeviceCMD.get_device_by_component_id(component_id)

        # in case custom event is present - execute it
        event = EventFactory.get(device.id, component_id, in_event)
        if event is not None:
            self.background_tasks.add_task(
                event,
                device,
                component_id,
                *args, **kwargs
            )

        # otherwise execute default event
        self.background_tasks.add_task(
            getattr(device.components[component_id], in_event),
            *args, **kwargs
        )
