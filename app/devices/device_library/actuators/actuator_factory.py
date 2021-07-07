from devices.device_library.actuators.base_class_actuator import Actuator
from devices.device_library.actuators.library.relayV1 import RelayV1


class ActuatorFactory:
    ACTUATORS = [RelayV1]

    @classmethod
    def get(cls, type: str, version: str) -> Actuator:
        for ac in cls.ACTUATORS:
            if ac.__type__ == type and ac.__version__ == version:
                return ac

        raise LookupError("No matching actutator found in codebase")