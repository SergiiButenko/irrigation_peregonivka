from devices.models.actuators import ActuatorListSQL, ActuatorSQL
from devices.dependencies import database, service_logger
from fastapi import Depends


class ActuatorsSQL:
    def __init__(self, service_logger=Depends(service_logger)):
        self.service_logger = service_logger

    async def get_by_id(self, device_id: str, actuator_id: int) -> ActuatorSQL:
        sql = """
        SELECT id, name, device_id, settings, category, type, version FROM components 
        WHERE id=:actuator_id AND device_id=:device_id;
        """
        result = await database.fetch_one(
            sql,
            values={"actuator_id": actuator_id, "device_id": device_id})
        return ActuatorSQL.parse_obj(result)

