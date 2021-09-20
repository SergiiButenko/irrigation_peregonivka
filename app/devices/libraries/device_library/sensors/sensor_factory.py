from devices.libraries.device_library.sensors.base_class_sensor import Sensor
from devices.libraries.device_library.sensors.library.DHT11V1 import DHT11V1
from devices.libraries.device_library.sensors.library.POWER_CURRENT import POWER_CURRENT


class SensorFactory:
    SENSORS = [DHT11V1, POWER_CURRENT]

    @classmethod
    def get(cls, type: str, version: str) -> Sensor:
        for ac in cls.SENSORS:
            if ac.__type__.lower() == type.lower() and ac.__version__.lower() == version.lower():
                return ac

        raise LookupError(f"No matching sensor '{type}':'{version}' found in codebase")