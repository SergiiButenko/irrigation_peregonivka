from typing import List, Optional
import uuid
from pydantic import BaseModel


class State(BaseModel):
    expected_state: str


class ActuatorSQL(BaseModel):
    id: int
    device_id: str
    name: str
    group_id: uuid.UUID
    category: str
    type: str
    version: str
    settings: Optional[dict] = None


class ActuatorListSQL(BaseModel):
    __root__: List[ActuatorSQL]
