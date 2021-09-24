from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    message: str


class RuleState(BaseModel):
    expected_state: str


class DeviceExpectedState(BaseModel):
    expected_state: str


class Rules(BaseModel):
    intervals: int
    time_wait: int
    time: int


class RulesActuators(BaseModel):
    device_id: str
    actuator_id: int
    rules: Rules


class RulesActuatorsList(BaseModel):
    actuators: List[RulesActuators]
    minutes_delay: int


class SensorValue(BaseModel):
    data: dict


class TelegramMessage(BaseModel):
    message: str
