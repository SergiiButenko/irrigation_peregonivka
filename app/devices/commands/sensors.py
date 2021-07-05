from fastapi import Depends
from devices.queries.sensors import SensorsNOSQL
from devices.dependencies import service_logger


class SensorsCMD:
    def __init__(
        self,
        SensorsNOSQL: SensorsNOSQL = Depends(),
        service_logger=Depends(service_logger),
    ):
        self.SensorsNOSQL = SensorsNOSQL
        self.service_logger = service_logger

    async def register_sensor_value_by_id(
        self, device_id: str, sensor_id: str, value: dict
    ) -> None:
        SensorsNOSQL.register_sensor_value_by_id(device_id, sensor_id, value)
