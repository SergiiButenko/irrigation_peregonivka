from typing import Optional
import uuid
from pydantic import BaseModel


class SensorValue(BaseModel):
    data: dict


class SensorSQL(BaseModel):
    id: int
    device_id: str
    name: str
    group_id: uuid.UUID
    category: str
    type: str
    version: str
    settings: Optional[dict] = None
