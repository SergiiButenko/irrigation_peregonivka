from typing import List, Optional
import uuid
from datetime import datetime

from pydantic import BaseModel


class DeviceSql(BaseModel):
    id: str
    description: str
    type: str
    version: str
    last_known_ip: Optional[str] = None
    updated: Optional[datetime] = None


class ComponentSql(BaseModel):
    id: int
    device_id: str
    name: str
    group_id: uuid.UUID
    category: str
    type: str
    version: str
    settings: Optional[dict] = None


class ComponentListSQL(BaseModel):
    __root__: List[ComponentSql]


class Message(BaseModel):
    message: str
