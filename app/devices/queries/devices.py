from devices.dependencies import database, service_logger
from devices.models.devices import DeviceSql
from fastapi import Depends


class DeviceSQL:
    def __init__(self, service_logger=Depends(service_logger)):
        self.service_logger = service_logger

    async def set_device_ip(self, device_id: str, device_ip: str) -> None:
        sql = """
        UPDATE devices SET last_known_ip=:device_ip WHERE id=:device_id;
        """
        self.service_logger.info(f"Executing {sql}")
        await database.execute(
            sql, values={"device_id": device_id, "device_ip": device_ip}
        )

    async def get_all_devices(self) -> DeviceSql:
        sql = """
        SELECT * FROM devices;
        """
        result = await database.fetch_all(sql)
        return DeviceSql.parse_obj(result)

    async def get_device(self, device_name: str) -> DeviceSql:
        sql = """
        SELECT * FROM devices WHERE name=:device_name;
        """
        result = await database.fetch_all(
            sql,
            values={"device_name": device_name}
        )
        return DeviceSql.parse_obj(result)
