from fastapi import Depends
from device_discovery.resources.device_dao import DeviceDAO
from device_discovery.service_providers.httpx_client import HttpxClient
from device_discovery.dependencies import service_logger


class PingToRegisterDeviceAllCmd:

    def __init__(self, DAO: DeviceDAO = Depends(),
                 logger=Depends(service_logger)):
        self.DAO = DAO
        self.logger = logger

    async def __call__(self):
        devices = await self.DAO.get_all_devices()
        for device in devices:
            await HttpxClient.post(url='http://'+device.ip+'/register')
