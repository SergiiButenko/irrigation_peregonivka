from devices.service_providers.device_logger import logger


class Actuator:
    def __init__(self, device, actuator_id) -> None:
        self.actuator_id = actuator_id
        self.device = device

    async def set_state(self, state, *args, **kwargs):
        return await self.device._set_actuator_state(
            self.actuator_id, state, *args, **kwargs
        )

    async def get_state(self):
        return self.device._get_actuator_state(self.actuator_id)
