from devices.libraries.device_library.devices.device_factory import DeviceFactory
from devices.libraries.device_library.devices.base_class_device import Device
from devices.models.devices import DeviceSql
from starlette.routing import NoMatchFound
from devices.queries.devices import DeviceQRS
from devices.service_providers.httpx_client import HttpxClient
from devices.service_providers.device_logger import logger

class DeviceCMD:

    @staticmethod
    async def ping_to_register_device_by_id(device_id: str) -> None:
        device = await DeviceQRS.get_device(device_id)
        await HttpxClient.post(url="http://" + device.ip + "/register")

    @staticmethod
    async def ping_to_register_devices():
        devices = await DeviceQRS.get_all_devices()
        for device in devices:
            await HttpxClient.post(
                url="http://" + device.ip + "/register"
            )
    
    @staticmethod
    async def get_device_IP_by_id(device_id) -> DeviceSql:
        _device = await DeviceQRS.get_device(device_id)
        if _device is None:
            raise NoMatchFound(f"No device id {device_id} found")

        return _device.ip


    @staticmethod
    async def send_message_to_device(
        device_id: str,
        message: dict
    ) -> bool:
        base_url = DeviceCMD.get_device_IP_by_id(device_id)
        HttpxClient.post(url="http://" + base_url + "/messages", json=message)

        return True

    @staticmethod
    async def get_device_by_id(device_id: str) -> Device:
        _deviceSQL = await DeviceQRS.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        return await _device.init(device_id)

    @staticmethod
    async def get_device_by_component_id(component_id: str) -> Device:
        _deviceSQL = await DeviceQRS.get_device_by_component_id(component_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        return await _device.init(_deviceSQL.id)

    @staticmethod
    async def get_component_state(device_id: str, component_id: int) -> str:
        device = await DeviceCMD.get_device_by_id(device_id)
        return await device.components[component_id].get_state()

    @staticmethod
    async def set_component_state(device_id: str, component_id: int, state) -> str:
        device = await DeviceCMD.get_device_by_id(device_id)
        return await device.components[component_id].set_state(state)