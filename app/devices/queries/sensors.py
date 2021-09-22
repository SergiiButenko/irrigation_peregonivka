from devices.dependencies import get_sql_db, get_logger, get_mongo_db

from fastapi import Depends


class SensorQRS:
    def __init__(
        self,
        service_logger=Depends(get_logger),
        mongo_db=Depends(get_mongo_db),
        psql_db=Depends(get_sql_db),
    ):
        self.service_logger = service_logger
        self.mongo_db = mongo_db
        self.psql_db = psql_db

    async def register_sensor_value_by_id(
        self, device_id: str, sensor_id: str, data: dict
    ) -> None:
        self.service_logger.info(
            f"Registering data '{data}' for device_id:sensor_id '{device_id}:{sensor_id}'"
        )
        await self.mongo_db.register_sensor_data(device_id, sensor_id, data)

    async def get_sensor_values_by_id(
        self,
        device_id: str,
        sensor_id: str,
        filter: dict = None,
        sorting: list = [("date", "DESC")],
    ):
        self.service_logger.info(
            f"Getting data for device_id:sensor_id '{device_id}:{sensor_id}'"
        )
        return await self.mongo_db.get_latest_sensor_data(
            device_id, sensor_id, filter, sorting
        )