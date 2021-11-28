from devices.libraries.device_library.sensors.base_class_sensor import Sensor


class POWER_CURRENT(Sensor):
    __type__ = "POWER_CURRENT"
    __version__ = "v1"

    def __init__(self, device, actuator_id) -> None:
        super().__init__(device, actuator_id)
