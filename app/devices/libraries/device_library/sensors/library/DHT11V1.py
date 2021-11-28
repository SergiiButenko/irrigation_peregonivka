from devices.libraries.device_library.sensors.base_class_sensor import Sensor


class DHT11V1(Sensor):
    __type__ = "DHT11"
    __version__ = "v1"

    def __init__(self, device, actuator_id) -> None:
        super().__init__(device, actuator_id)
