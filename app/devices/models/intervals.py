from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime


class Interval(BaseModel):
    id: uuid.UUID
    device_component_id: uuid.UUID
    execution_time: datetime
    state: Optional[str] = None
    user_id: uuid.UUID
