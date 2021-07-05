from fastapi import Depends
from devices.queries.actuators import ActuatorsSQL
from devices.commands.devices import DeviceCMD
from devices.dependencies import service_logger, ahttp_client


class ActuatorCMD:
    def __init__(self,
                 ActuatorsSQL: ActuatorsSQL = Depends(),
                 DeviceCMD: DeviceCMD = Depends(),
                 service_logger=Depends(service_logger),
                 ahttp_client=Depends(ahttp_client)):
        self.ActuatorsSQL = ActuatorsSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger
        self.ahttp_client = ahttp_client

    async def set_actuator_state(
        self, device_id: str,
        actuator_id: str,
        state
    ) -> None:
        base_url = self.DeviceCMD.get_device_IP_by_id(device_id)

        await self.ahttp_client.post(
            url="http://" + base_url + "/state",
            params={"id": actuator_id, 'state': state.expected_state}
        )

    async def get_actuator_state(
        self,
        device_id: str,
        actuator_id: str
    ) -> str:
        base_url = self.DeviceCMD.get_device_IP_by_id(device_id)

        _state = await self.ahttp_client.get(
            url="http://" + base_url + "/state"
        )

        return _state['state'][actuator_id]
