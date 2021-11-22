from devices.libraries.device_library.devices.base_class_device import Device


class Device4chV1(Device):
    __type__ = 'Relay4ch'
    __version__ = 'v1'

    def __init__(self, id) -> None:
        super().__init__(id)
