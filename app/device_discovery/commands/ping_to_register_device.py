from fastapi import Depends
from device_discovery.resources.device_dao import DeviceDAO
from device_discovery.service_providers.httpx_client import HttpxClient
from device_discovery.dependencies import service_logger


class PingToRegisterDeviceCmd:

    def __init__(self, DeviceDAO: DeviceDAO = Depends(),
                 logger=Depends(service_logger)):
        self.DAO = DeviceDAO
        self.logger = logger

    async def __call__(self, device_id):
        device = await self.DAO.get_device(device_id)
        await HttpxClient.post(url='http://'+device.ip+'/register')
