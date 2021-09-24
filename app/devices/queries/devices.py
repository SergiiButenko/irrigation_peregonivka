from devices.models.devices import ComponentSql, DeviceSql, TelegramUser
from devices.schemas.schema import DeviceExpectedState
from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger


class DeviceSQL:

    @staticmethod
    async def set_device_ip(device_id: str, device_ip: str) -> None:
        sql = """
        UPDATE devices SET last_known_ip=:device_ip WHERE id=:device_id;
        """
        logger.info(f"Executing {sql}")
        await psql_db.execute(
            sql, values={"device_id": device_id, "device_ip": device_ip}
        )

    @staticmethod
    async def get_all_devices() -> DeviceSql:
        sql = """
        SELECT * FROM devices;
        """
        result = await psql_db.fetch_all(sql)
        return DeviceSql.parse_obj(result)

    @staticmethod
    async def get_device(device_id: str) -> DeviceSql:
        sql = """
        SELECT * FROM devices WHERE id=:device_id;
        """
        result = await psql_db.fetch_one(sql, values={"device_id": device_id})
        return DeviceSql.parse_obj(result)

    @staticmethod
    async def get_component_by_id(
        device_id: str, component_id: int
    ) -> ComponentSql:
        sql = """
        SELECT id, device_id, name, group_id, category, type, version, settings, usage_type FROM components 
        WHERE id=:component_id AND device_id=:device_id;
        """
        result = await psql_db.fetch_one(
            sql, values={"component_id": component_id, "device_id": device_id}
        )
        return ComponentSql.parse_obj(result)

    @staticmethod
    async def get_expected_actuator_state(device_id: str, actuator_id: int) -> DeviceExpectedState:
        sql = """
        """
        result = await psql_db.fetch_one(
            sql, values={"actuator_id": actuator_id, "device_id": device_id}
        )
        return DeviceExpectedState.parse_obj(result)

    @staticmethod
    async def get_linked_telegram_user(device_id: str, component_id: int) -> TelegramUser:
        sql = """SELECT telegram_user FROM components
        WHERE id=:component_id AND device_id=:device_id;
        """
        result = await psql_db.fetch_one(
            sql, values={"component_id": component_id, "device_id": device_id}
        )
        return TelegramUser.parse_obj(result)
