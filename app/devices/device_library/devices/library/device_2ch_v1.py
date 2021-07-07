from devices.device_library.devices.base_class_device import Device


class Device2chV1(Device):
    __type__ = 'Relay2ch'
    __version__ = 'v1'

    def __init__(self, device_id) -> None:
        super().__init__(device_id)
