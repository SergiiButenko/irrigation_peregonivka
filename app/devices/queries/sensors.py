from devices.models.sensors import SensorSQL
from devices.dependencies import service_logger, mongo_db, database
from devices.models.devices import DeviceSql
from fastapi import Depends


class SensorsNOSQL:
    def __init__(
        self,
        service_logger=Depends(service_logger),
        mongo=Depends(mongo_db)
    ):
        self.service_logger = service_logger
        self.mongo = mongo

    async def register_sensor_value_by_id(
        self, device_id: str, sensor_id: str, data: dict
    ) -> None:
        self.service_logger.info(
            f"Registering data '{data}' for \
            device_id:sensor_id '{device_id}:{sensor_id}'"
        )
        await self.mongo.register_sensor_data(device_id, sensor_id, data)

    async def get_values_by_id(
        self,
        device_id: str,
        sensor_id: str,
        minutes_from_now: int,
        function: str,
        sorting: str,
    ) -> DeviceSql:
        self.service_logger.info(
            f"Getting data for device_id:sensor_id '{device_id}:{sensor_id}'"
        )
        return await self.mongo.get_latest_sensor_data(
            device_id, sensor_id, minutes_from_now, function, sorting
        )

    async def get_by_id(self, device_id: str, sensor_id: int) -> SensorSQL:
        sql = """
        SELECT * FROM components WHERE device_id=:device_id AND id=:sensor_id;
        """
        self.service_logger.info(f"Executing {sql}")
        await database.execute(
            sql, values={"device_id": device_id, "sensor_id": sensor_id}
        )