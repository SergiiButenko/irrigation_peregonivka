from logging import log
from devices.queries.devices import DeviceQRS
from starlette.routing import NoMatchFound
from devices.libraries.device_library.sensors.sensor_factory import SensorFactory
from devices.libraries.device_library.actuators.actuator_factory import ActuatorFactory
from devices.enums.devices import SensorEnum, ActuatorsEnum
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.device_logger import logger


class Device:

    def __init__(
        self,
        device_id,
    ) -> None:
        self.device_id = device_id
        self.components = {}
        self.device = {}

    @staticmethod
    async def get_device(device_id: str):
        _device = Device(device_id)
        await _device._init_device()
        return await _device._init_components()

    async def _set_actuator_state(self, actuator_id: int, state: str) -> dict:
        await HttpxClient.post_with_raise(
            url=f"{self.device.last_known_ip}/actuators/{actuator_id}",
            json={'expected_state': state}
        )

    async def _get_actuator_state(self, actuator_id: int) -> dict:
        await HttpxClient.get_with_raise(
            url=f"{self.device.last_known_ip}/actuators/{actuator_id}"
        )

    async def _get_sensor_data(self, sensor_id: int) -> dict:
        await HttpxClient.get_with_raise(
            url=f"{self.device.last_known_ip}/sensors/{sensor_id}"
        )

    async def _init_device(self):
        self.device = await DeviceQRS.get_device(self.device_id)
        return self

    async def _init_components(self) -> None:
        components = await DeviceQRS.get_components_by_device_id(self.device_id)
        
        for c in components.__root__:
            if c.category == ActuatorsEnum.category:
                _actuator = ActuatorFactory.get(c.type, c.version)
                self.components[c.id] = _actuator(self, c.id)
            elif c.category == SensorEnum.category:
                _sensor = SensorFactory.get(c.type, c.version)
                self.components[c.id] = _sensor(self, c.id)
            else:
                raise NoMatchFound("No component type registered")

        return self
