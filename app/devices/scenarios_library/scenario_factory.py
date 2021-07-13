
from devices.models.scenarios.scenario import Scenario
import os
from devices.config.config import Config


class ScenarioFactory:
    SCENARIOS = [
        "cesspoll_relay_sensor1.yaml",
        # "garden_switcher1.yaml",
        # "irrigation_relay1.yaml",
    ]

    @classmethod
    def get(cls, device_id: str, component_id: int):
        for sc in cls.SCENARIOS:
            _path = os.path.join(Config.SCENARIOS_PATH, sc)
            _scenario = Scenario(_path).parse_scenario()
            return _scenario
            


