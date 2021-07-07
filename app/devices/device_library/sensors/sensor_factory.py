from devices.device_library.sensors.base_class_sensor import Sensor
from devices.device_library.sensors.library.DHT11V1 import DHT11V1


class SensorFactory:
    SENSORS = [DHT11V1]

    @classmethod
    def get(cls, type: str, version: str) -> Sensor:
        for ac in cls.SENSORS:
            if ac.__type__.lower() == type.lower() and ac.__version__.lower() == version.lower():
                return ac

        raise LookupError("No matching sensor found in codebase")