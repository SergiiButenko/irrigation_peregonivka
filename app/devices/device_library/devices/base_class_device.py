from devices.device_library.actuators.ActuatorFactory import ActuatorFactory
from devices.enums.sensors import SensorEnum
from devices.enums.actuators import ActuatorsEnum
from devices.models.devices import ComponentSql


class Device:

    def __init__(self, device_id) -> None:
        self.device_id = device_id
        self.actuators = []
        self.sensors = []

    def _set_actuator_state(self, actuator_id: int) -> dict:
        return "NEW STATE"

    def _get_actuator_state(self, actuator_id: int) -> dict:
        return "OLD STATE"

    # def _get_sensor_data(self, sensor_id: int) -> dict:
    #     #send request to sensor
    #     pass

    def init_components(self) -> None:
        sql = """
        SELECT * FROM components WHERE device_id:=device_id;
        """
        _results = database.execute(sql)

        components = ComponentSql.parse_obj(_results)

        for c in components:
            if c.type == ActuatorsEnum.type:
                _actuator = ActuatorFactory.get(c.version)
                self.actuators.append(_actuator(self, c.id))

