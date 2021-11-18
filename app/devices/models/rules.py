from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


class Rule(BaseModel):
    id: uuid.UUID
    interval_id: uuid.UUID
    device_id: Optional[str] = None
    component_id: Optional[int] = None
    device_component_id: uuid.UUID
    expected_state: str
    execution_time: datetime
    state: str

class Rules(BaseModel):
    __root__: List[Rule]


class DashboardIrrigationRule(BaseModel):
    id: uuid.UUID
    name: str
    state: str
    execution_time: datetime


class DashboardIrrigationRules(BaseModel):
    __root__: List[DashboardIrrigationRule]
