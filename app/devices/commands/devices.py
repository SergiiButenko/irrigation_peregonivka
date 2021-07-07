from devices.device_library.devices.device_factory import DeviceFactory
from devices.device_library.devices.base_class_device import Device
from devices.models.devices import DeviceSql, ComponentSql
from fastapi import Depends
from starlette.routing import NoMatchFound
from devices.queries.devices import DeviceSQL
from devices.dependencies import service_logger, ahttp_client


class DeviceCMD:
    def __init__(
        self,
        DeviceSQL: DeviceSQL = Depends(),
        service_logger=Depends(service_logger),
        ahttp_client=Depends(ahttp_client),
    ):
        self.DeviceSQL = DeviceSQL
        self.service_logger = service_logger
        self.ahttp_client = ahttp_client

    async def ping_to_register_device_by_id(self, device_id: str) -> None:
        device = await self.DeviceSQL.get_device(device_id)
        await self.ahttp_client.post(url="http://" + device.ip + "/register")

    async def ping_to_register_devices(self):
        devices = await self.DeviceSQL.get_all_devices()
        for device in devices:
            await self.ahttp_client.post(
                url="http://" + device.ip + "/register"
            )

    async def register_device_by_id(
        self,
        device_id: str,
        device_ip: str
    ) -> bool:
        return await self.DeviceSQL.set_device_ip(device_id, device_ip)

    async def get_device_IP_by_id(self, device_id) -> DeviceSql:
        _device = await self.DeviceSQL.get_device(device_id)
        if _device is None:
            raise NoMatchFound(f"No device id {device_id} found")

        return _device.ip

    async def get_component_by_id(
        self, device_id: str, component_id: str
    ) -> ComponentSql:
        _component = await self.DeviceSQL.get_component_by_id(component_id)
        if _component.device_id != device_id:
            raise ValueError(
                f"Device id '{device_id}' is not expected \
                    '{_component.device_id}' one"
            )

        return _component

    async def send_message_to_device(
        self,
        device_id: str,
        message: dict
    ) -> bool:
        base_url = self.get_device_IP_by_id(device_id)
        ahttp_client.post(url="http://" + base_url + "/messages", json=message)

        return True

    async def get_device_by_id(self, device_id: str) -> Device:
        _deviceSQL = await self.DeviceSQL.get_device(device_id)
        _device = DeviceFactory.get(_deviceSQL.type, _deviceSQL.version)
        return await _device(device_id).init_components()
