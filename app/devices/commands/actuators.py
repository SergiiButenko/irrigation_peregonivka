from devices.queries.devices import DeviceSQL
from devices.device_library.devices.device_factory import DeviceFactory
from fastapi import Depends
from devices.queries.actuators import ActuatorsSQL
from devices.commands.devices import DeviceCMD
from devices.dependencies import service_logger, ahttp_client


class ActuatorCMD:
    def __init__(self,
                 ActuatorsSQL: ActuatorsSQL = Depends(),
                 DeviceSQL: DeviceSQL = Depends(),
                 DeviceCMD: DeviceCMD = Depends(),
                 service_logger=Depends(service_logger),
                 ahttp_client=Depends(ahttp_client)):
        self.ActuatorsSQL = ActuatorsSQL
        self.DeviceSQL = DeviceSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger
        self.ahttp_client = ahttp_client

    async def set_actuator_state(
        self, device_id: str,
        actuator_id: str,
        state
    ) -> None:
        _deviceSQL = self.DeviceSQL.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        device = _device(device_id)
        device.init_components()
        return await device.actuators[actuator_id].set_state(state)

    async def get_actuator_state(
        self,
        device_id: str,
        actuator_id: str
    ) -> str:
        _deviceSQL = self.DeviceSQL.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        device = _device(device_id).init_components()
        return await device.actuators[actuator_id].get_state()
