import uuid
from datetime import datetime

from pydantic import BaseModel


class DeviceSql(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    last_known_ip: str
    updated: datetime
