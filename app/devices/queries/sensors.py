from devices.schemas.schema import SensorData
from devices.service_providers.device_logger import logger
from devices.service_providers.mongo_db import mongo_db


class SensorQRS:
    @staticmethod
    async def register_sensor_value_by_id(component_id: str, data: dict) -> None:
        logger.info(f"Registering data '{data}' for component_id '{component_id}'")
        await mongo_db.register_sensor_data(component_id, data)

    @staticmethod
    async def get_sensor_values_by_id(
        component_id: str,
        filter: dict = None,
        sorting: list = [("date", "DESC")],
        limit: int = 10,
    ) -> SensorData:
        logger.info(f"Getting data for component id '{component_id}'")
        return await mongo_db.get_latest_sensor_data(component_id, filter, sorting, limit)