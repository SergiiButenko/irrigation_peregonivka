from fastapi import BackgroundTasks
from devices.events_library.event_factory import EventFactory
from devices.queries.devices import DeviceSQL
from fastapi import Depends
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger, get_config


class EventsCMD:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        DeviceSQL: DeviceSQL = Depends(),
        DeviceCMD: DeviceCMD = Depends(),
        service_logger=Depends(get_logger),
        config=Depends(get_config()),
    ):
        self.DeviceSQL = DeviceSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger
        self.config = config
        self.background_tasks = background_tasks

    async def try_execute(self, device_id: str, sensor_id: int, event: str) -> None:
        event = EventFactory.get(device_id, sensor_id, event)
        self.background_tasks.add_task(event)
