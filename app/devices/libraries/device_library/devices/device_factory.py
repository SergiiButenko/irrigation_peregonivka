from devices.libraries.device_library.devices.base_class_device import Device
from devices.libraries.device_library.devices.library.device_2ch_v1 import Device2chV1
from devices.libraries.device_library.devices.library.device_4ch_v1 import Device4chV1
from devices.libraries.device_library.devices.library.device_8ch_v1 import Device8chV1


class DeviceFactory:
    DEVICES = [Device2chV1, Device4chV1, Device8chV1]

    @classmethod
    def get(cls, type: str, version: str) -> Device:
        for ac in cls.DEVICES:
            if ac.__type__.lower() == type.lower() and ac.__version__.lower() == version.lower():
                return ac

        raise LookupError("No matching device found in codebase")