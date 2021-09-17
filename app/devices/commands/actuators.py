from devices.queries.devices import DeviceSQL
from devices.device_library.devices.device_factory import DeviceFactory
from fastapi import Depends
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger


class ActuatorCMD:
    def __init__(
        self,
        DeviceSQL: DeviceSQL = Depends(),
        DeviceCMD: DeviceCMD = Depends(),
        service_logger=Depends(get_logger),
    ):
        self.DeviceSQL = DeviceSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger

    async def set_actuator_state(self, device_id: str, actuator_id: int, state) -> None:
        _deviceSQL = await self.DeviceSQL.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        device = await _device(device_id).init_components()
        return await device.actuators[actuator_id].set_state(state)

    async def get_actuator_state(self, device_id: str, actuator_id: int) -> str:
        _deviceSQL = await self.DeviceSQL.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        device = await _device(device_id).init_components()
        return await device.actuators[actuator_id].get_state()
