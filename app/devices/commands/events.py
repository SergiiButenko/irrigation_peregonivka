from fastapi import Depends, BackgroundTasks
from devices.libraries.events_library.event_factory import EventFactory
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger, get_config


class EventsCMD:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        DeviceCMD: DeviceCMD = Depends(),
        EventFactory: EventFactory = Depends(),
        service_logger=Depends(get_logger),
        config=Depends(get_config()),
    ):
        self.DeviceCMD = DeviceCMD
        self.EventFactory = EventFactory
        self.service_logger = service_logger
        self.config = config
        self.background_tasks = background_tasks

    async def try_execute(self, device_id: str, sensor_id: int, event: str) -> None:
        device = await self.DeviceCMD.get_device_by_id(device_id)
        event = await self.EventFactory.get(device, sensor_id, event)
        self.background_tasks.add_task(event)
