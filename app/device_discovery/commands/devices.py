from fastapi import Depends
from device_discovery.queries.devices import DeviceSQL
from device_discovery.service_providers.httpx_client import HttpxClient
from device_discovery.dependencies import service_logger


class DeviceCMD:
    def __init__(self, DeviceSQL: DeviceSQL = Depends(),
                 service_logger=Depends(service_logger)):
        self.DeviceSQL = DeviceSQL
        self.service_logger = service_logger

    async def ping_to_register_device_by_id(self, device_id) -> None:
        device = await self.DeviceSQL.get_device(device_id)
        await HttpxClient.post(url='http://'+device.ip+'/register')

    async def ping_to_register_devices(self):
        devices = await self.DeviceSQL.get_all_devices()
        for device in devices:
            await HttpxClient.post(url='http://'+device.ip+'/register')

    async def register_device_by_id(self, device_id, device_ip) -> bool:
        return await self.DeviceSQL.set_device_ip(device_id, device_ip)
