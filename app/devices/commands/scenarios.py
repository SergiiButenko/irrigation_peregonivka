from devices.scenarios_library.scenario_factory import ScenarioFactory
from devices.queries.devices import DeviceSQL
from devices.device_library.devices.device_factory import DeviceFactory
from fastapi import Depends
from devices.commands.devices import DeviceCMD
from devices.dependencies import service_logger, get_config


class ScenariosCMD:
    def __init__(
        self,
        DeviceSQL: DeviceSQL = Depends(),
        DeviceCMD: DeviceCMD = Depends(),
        service_logger=Depends(service_logger),
        config=Depends(get_config()),
    ):
        self.DeviceSQL = DeviceSQL
        self.DeviceCMD = DeviceCMD
        self.service_logger = service_logger
        self.config = config

    async def analyse_sensor_data(self, device_id: str, sensor_id: int) -> None:
        return ScenarioFactory.get(device_id, sensor_id)