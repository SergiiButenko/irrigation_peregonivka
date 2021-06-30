from devices.dependencies import service_logger, mongo_db
from devices.models.devices import DeviceSql
from fastapi import Depends


class SensorsNOSQL:
    def __init__(self, service_logger=Depends(service_logger)):
        self.service_logger = service_logger

    async def register_sensor_value_by_id(self, device_id: str, sensor_id: str, data: dict) -> None:
        self.service_logger.info(f"Registering data '{data}' for device_id:sensor_id '{device_id}:{sensor_id}'")
        await mongo_db.register_sensor_data(
            device_id, sensor_id, data
        )

    async def get_values_by_id(self, device_id: str, sensor_id: str, minutes_from_now: int, function: str, sorting: str) -> DeviceSql:
        self.service_logger.info(f"Getting data for device_id:sensor_id '{device_id}:{sensor_id}'")
        return await mongo_db.get_latest_sensor_data(
            device_id, sensor_id, minutes_from_now, function, sorting
        )
