import yaml
from devices.models.scenarios.events.base_event import BaseEvent


class EventRegisterData(BaseEvent, yaml.YAMLObject):
    yaml_tag = '!register_data'

    def __init__(self, conditions: dict, actions: dict) -> None:
        super().__init__(conditions, actions)
