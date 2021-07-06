from devices.device_library.actuators.base_class_actuator import Actuator
from devices.device_library.actuators import library


class ActuatorFactory:

    @staticmethod
    def get(type: str, version: str) -> Actuator:
        for ac in library:
            if ac.__type__ == type and ac.__version__ == version:
                return ac

        raise LookupError("No matching actutator found in codebase")