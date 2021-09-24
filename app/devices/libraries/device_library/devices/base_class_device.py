from starlette.routing import NoMatchFound
from devices.libraries.device_library.sensors.sensor_factory import SensorFactory
from devices.models.devices import ComponentSql
from devices.libraries.device_library.actuators.actuator_factory import ActuatorFactory
from devices.enums.devices import SensorEnum, ActuatorsEnum
from devices.service_providers.sql_db import psql_db


class Device:

    def __init__(
        self,
        device_id,
    ) -> None:
        self.device_id = device_id
        self.components = {}
        self.database = psql_db

    async def _set_actuator_state(self, actuator_id: int, state: str) -> dict:
        return state

    async def _get_actuator_state(self, actuator_id: int) -> dict:
        return 1

    async def _get_sensor_data(self, sensor_id: int) -> dict:
        return "{data: {temp: 27}"

    async def init_components(self) -> None:
        sql = """
        SELECT * FROM components WHERE device_id=:device_id;
        """
        _results = await self.database.fetch_all(
            sql,
            values={"device_id": self.device_id}
        )

        components = list()
        for _result in _results:
            components.append(ComponentSql.parse_obj(_result))

        for c in components:
            if c.category == ActuatorsEnum.category:
                _actuator = ActuatorFactory.get(c.type, c.version)
                self.components[c.id] = _actuator(self, c.id)
            elif c.category == SensorEnum.category:
                _sensor = SensorFactory.get(c.type, c.version)
                self.components[c.id] = _sensor(self, c.id)
            else:
                raise NoMatchFound("No component type registered")

        return self
