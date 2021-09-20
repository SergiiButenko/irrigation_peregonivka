from devices.dependencies import psql_db, get_logger, mongo_db
from devices.models.devices import ComponentSql, DeviceSql, DeviceExpectedState, TelegramUser
from fastapi import Depends


class DeviceSQL:
    def __init__(
        self,
        service_logger=Depends(get_logger),
        mongo_db=Depends(mongo_db),
        psql_db=Depends(psql_db),
    ):
        self.service_logger = service_logger
        self.mongo_db = mongo_db
        self.psql_db = psql_db

    async def set_device_ip(self, device_id: str, device_ip: str) -> None:
        sql = """
        UPDATE devices SET last_known_ip=:device_ip WHERE id=:device_id;
        """
        self.service_logger.info(f"Executing {sql}")
        await self.psql_db.execute(
            sql, values={"device_id": device_id, "device_ip": device_ip}
        )

    async def get_all_devices(self) -> DeviceSql:
        sql = """
        SELECT * FROM devices;
        """
        result = await self.psql_db.fetch_all(sql)
        return DeviceSql.parse_obj(result)

    async def get_device(self, device_id: str) -> DeviceSql:
        sql = """
        SELECT * FROM devices WHERE id=:device_id;
        """
        result = await self.psql_db.fetch_one(sql, values={"device_id": device_id})
        return DeviceSql.parse_obj(result)

    async def get_component_by_id(
        self, device_id: str, component_id: int
    ) -> ComponentSql:
        sql = """
        SELECT id, device_id, name, group_id, category, type, version, settings FROM components 
        WHERE id=:actuator_id AND device_id=:device_id;
        """
        result = await self.psql_db.fetch_one(
            sql, values={"actuator_id": component_id, "device_id": device_id}
        )
        return ComponentSql.parse_obj(result)

    async def get_expected_actuator_state(self, device_id: str, actuator_id: int) -> DeviceExpectedState:
        sql = """
        """
        result = await self.psql_db.fetch_one(
            sql, values={"actuator_id": actuator_id, "device_id": device_id}
        )
        return DeviceExpectedState.parse_obj(result)

    async def get_linked_telegram_user(self, device_id: str, component_id: int) -> TelegramUser:
        sql = """SELECT telegram_user FROM components
        WHERE id=:component_id AND device_id=:device_id;
        """
        result = await self.psql_db.fetch_one(
            sql, values={"component_id": component_id, "device_id": device_id}
        )
        return TelegramUser.parse_obj(result)
