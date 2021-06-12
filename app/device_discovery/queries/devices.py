from device_discovery.models.devices import DeviceSql
from device_discovery.dependencies import database


class DeviceSQL:
    @staticmethod
    async def set_device_ip(device_name: str, device_ip: str) -> None:
        sql = """
        UPDATE devices SET ip=:device_ip WHERE name=:device_name;
        """
        await database.execute(
            sql, values={"device_name": device_name, "ip": device_ip}
        )

    @staticmethod
    async def get_all_devices() -> DeviceSql:
        sql = """
        SELECT * FROM devices;
        """
        result = await database.fetch_all(sql)
        return DeviceSql.parse_obj(result)

    @staticmethod
    async def get_device(device_name: str) -> DeviceSql:
        sql = """
        SELECT * FROM devices WHERE name=:device_name;
        """
        result = await database.fetch_all(
            sql, values={"device_name": device_name}
        )
        return DeviceSql.parse_obj(result)
