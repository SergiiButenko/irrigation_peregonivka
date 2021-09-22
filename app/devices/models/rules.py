from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


class Rule(BaseModel):
    id: uuid.UUID
    interval_uuid: uuid.UUID
    device_id: str
    actuator_id: int
    expected_state: str
    execution_time: datetime
    state: str


class Rules(BaseModel):
    __root__: List[Rule]
