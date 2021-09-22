from datetime import date, timedelta
from devices.queries.devices import DeviceSQL
from fastapi import Depends
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger, get_config
from devices.models.rules import Rule, Rules


class RulesCMD:
    def __init__(
        self,
        DeviceCMD: DeviceCMD = Depends(),
        DeviceSQL: DeviceSQL = Depends(),
        service_logger=Depends(get_logger),
        config=Depends(get_config()),
    ):
        self.DeviceCMD = DeviceCMD
        self.DeviceSQL = DeviceSQL
        self.service_logger = service_logger
        self.config = config

    async def _form_rule():
        pass

    async def create_rules(self, rules: dict) -> Rules:
    # {"actuators": [
    #     {"device_id":"23",
    #     "actuator_id": 1,
    #     "settings": {
    #         "time":"15",
    #         "intervals":"2",
    #         "time_wait":"15"
    #         }
    #     }],
    # "hours_delay":9
    # }
        time_start = datetime.now + timedelta(hours=rules['hours_delay'])
        actuators_list = rules['actuators']
