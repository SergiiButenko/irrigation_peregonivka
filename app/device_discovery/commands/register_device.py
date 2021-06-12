from fastapi import Depends
from device_discovery.resources.device_dao import DeviceDAO
from device_discovery.dependencies import service_logger


class RegisterDeviceCmd:

    def __init__(self, DeviceDAO: DeviceDAO = Depends(),
                 logger=Depends(service_logger)):
        self.DAO = DeviceDAO
        self.logger = logger

    async def __call__(self, device_id, ip):
        await self.DAO.set_device_ip(device_id, ip)
