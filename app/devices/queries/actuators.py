from devices.models.actuators import ActuatorListSQL, ActuatorSQL
from devices.dependencies import _psql_db, get_logger
from fastapi import Depends


class ActuatorsSQL:
    def __init__(self, service_logger=Depends(get_logger)):
        self.service_logger = service_logger

    async def get_by_id(self, device_id: str, actuator_id: int) -> ActuatorSQL:
        sql = """
        SELECT id, device_id, name, group_id, category, type, version, settings FROM components 
        WHERE id=:actuator_id AND device_id=:device_id;
        """
        result = await database.fetch_one(
            sql,
            values={"actuator_id": actuator_id, "device_id": device_id})
        return ActuatorSQL.parse_obj(result)

