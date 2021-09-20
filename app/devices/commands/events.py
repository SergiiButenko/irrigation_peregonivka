from devices.queries.sensors import SensorQRS
from devices.queries.devices import DeviceSQL
from fastapi import Depends, BackgroundTasks
from devices.libraries.events_library.event_factory import EventFactory
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger, get_config


class EventsCMD:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        DeviceCMD: DeviceCMD = Depends(),
        DeviceSQL: DeviceSQL = Depends(),
        service_logger=Depends(get_logger),
        config=Depends(get_config()),
        sensor_qrs: SensorQRS = Depends(SensorQRS),
    ):
        self.background_tasks = background_tasks
        self.DeviceCMD = DeviceCMD
        self.DeviceSQL = DeviceSQL
        self.service_logger = service_logger
        self.config = config
        self.sensor_qrs = sensor_qrs

    async def try_execute(self, device_id: str, sensor_id: int, event: str) -> None:
        device = await self.DeviceCMD.get_device_by_id(device_id)
        event = EventFactory.get(device, sensor_id, event)
        self.background_tasks.add_task(
            event,
            device,
            sensor_id,
            self.DeviceCMD,
            self.DeviceSQL,
            self.sensor_qrs,
            self.service_logger,
        )
