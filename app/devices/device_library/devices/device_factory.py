from devices.device_library.devices.base_class_device import Device
from devices.device_library.devices import library


class DeviceFactory:

    @staticmethod
    def get(type: str, version: str) -> Device:
        for ac in library:
            if ac.__type__ == type and ac.__version__ == version:
                return ac

        raise LookupError("No matching device found in codebase")