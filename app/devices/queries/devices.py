from devices.models.devices import DeviceSql, TelegramUser
from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger


class DeviceQRS:
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
    async def get_device_by_component_id(component_id: str) -> DeviceSql:
        sql = """
        SELECT d.* FROM devices d
        JOIN device_components dc ON d.id = dc.device_id
        WHERE dc.id=:component_id;
        """
        result = await psql_db.fetch_one(sql, values={"component_id": component_id})

        return DeviceSql.parse_obj(result)

    @staticmethod
    async def get_linked_telegram_user(component_id: str) -> TelegramUser:
        sql = """SELECT telegram_user FROM device_components
        WHERE id=:component_id;
        """
        result = await psql_db.fetch_one(sql, values={"component_id": component_id})
        return TelegramUser.parse_obj(result)
