from fastapi import Depends
from devices.queries.sensors import SensorsNOSQL
from devices.dependencies import get_logger
from devices.queries.devices import DeviceSQL
from devices.commands.devices import DeviceCMD


class SensorsCMD:
    def __init__(
        self,
        DeviceSQL: DeviceSQL = Depends(),
        DeviceCMD: DeviceCMD = Depends(),
        service_logger=Depends(get_logger),
        sensors_db: SensorsNOSQL = Depends(SensorsNOSQL),
    ):
        self.DeviceSQL = DeviceSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger
        self.sensors_db = sensors_db

    async def get_sensor_state(self, device_id: str, sensor_id: int) -> str:
        device = await self.DeviceCMD.get_device_by_id(device_id)
        return await device.sensors[sensor_id].get_state()

    async def register_sensor_value_by_id(
        self, device_id: str, sensor_id: str, value: dict
    ) -> None:
        await self.sensors_db.register_sensor_value_by_id(device_id, sensor_id, value)
