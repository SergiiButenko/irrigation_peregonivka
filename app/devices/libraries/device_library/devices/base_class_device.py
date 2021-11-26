from devices.queries.components import ComponentsQRS
from devices.queries.devices import DeviceQRS
from starlette.routing import NoMatchFound
from devices.libraries.device_library.sensors.sensor_factory import SensorFactory
from devices.libraries.device_library.actuators.actuator_factory import ActuatorFactory
from devices.enums.devices import SensorEnum, ActuatorsEnum
from devices.service_providers.httpx_client import HttpxClient


class Device:

    def __init__(
        self,
        id,
    ) -> None:
        self.id = id
        self.components = {}
        self.device = {}
        self._DUMMY_STATE = None

    @staticmethod
    async def init(id: str):
        _device = Device(id)
        await _device._init_device()
        return await _device._init_components()

    async def _set_actuator_state(self, actuator_id: int, state: str) -> dict:
        self._DUMMY_STATE = state
        return self._DUMMY_STATE
        await HttpxClient.post_with_raise(
            url=f"{self.device.last_known_ip}/actuators/{actuator_id}",
            json={'expected_state': state}
        )

    async def _get_actuator_state(self, actuator_id: int) -> dict:
        return self._DUMMY_STATE
        await HttpxClient.get_with_raise(
            url=f"{self.device.last_known_ip}/actuators/{actuator_id}"
        )

    async def _get_sensor_data(self, sensor_id: int) -> dict:
        await HttpxClient.get_with_raise(
            url=f"{self.device.last_known_ip}/sensors/{sensor_id}"
        )

    async def _init_device(self):
        self.device = await DeviceQRS.get_device(self.id)
        return self

    async def _init_components(self) -> None:
        components = await ComponentsQRS.get_components_by_device_id(self.id)

        for c in components.__root__:
            if c.category == ActuatorsEnum.category:
                _actuator = ActuatorFactory.get(c.type, c.version)
                self.components[str(c.id)] = _actuator(self, c.id)
            elif c.category == SensorEnum.category:
                _sensor = SensorFactory.get(c.type, c.version)
                self.components[str(c.id)] = _sensor(self, c.id)
            else:
                raise NoMatchFound("No component type registered")

        return self
