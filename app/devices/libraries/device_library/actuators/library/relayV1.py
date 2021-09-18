from devices.libraries.device_library.actuators.base_class_actuator import Actuator


class RelayV1(Actuator):
    __type__ = 'relay'
    __version__ = 'v1'

    def __init__(self, device, actuator_id) -> None:
        super().__init__(device, actuator_id)
