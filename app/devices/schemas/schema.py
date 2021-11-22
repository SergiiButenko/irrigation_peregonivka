from pydantic.types import UUID4
from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    message: str


class RuleState(BaseModel):
    expected_state: str


class IntervalState(RuleState):
    pass


class ComponentExpectedState(BaseModel):
    expected_state: Optional[str] = None


class Rules(BaseModel):
    intervals: int
    time_wait: int
    time: int


class RulesComponents(BaseModel):
    component_id: UUID4
    rules: Rules


class RulesComponentsList(BaseModel):
    components: List[RulesComponents]
    minutes_delay: int


class RulesComponentsIntervals(BaseModel):
    component_id: UUID4
    interval_id: UUID4
    rules: Rules


class RulesComponentsIntervalsList(BaseModel):
    components: List[RulesComponentsIntervals]
    minutes_delay: int


class SensorValue(BaseModel):
    data: dict


class TelegramMessage(BaseModel):
    message: str
