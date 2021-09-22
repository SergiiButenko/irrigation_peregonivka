from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime


class Rule(BaseModel):
    id: uuid.UUID
    next_rule: uuid.UUID
    device_id: str
    actuator_id: int
    expected_state: dict
    execution_time: datetime
    state: str


class Rules(BaseModel):
    __root__: List[Rule]
