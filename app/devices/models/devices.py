import uuid
from datetime import datetime

from pydantic import BaseModel


class DeviceSql(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    last_known_ip: str
    updated: datetime


class ComponentSql(BaseModel):
    id: uuid.UUID
    name: str
    device_id: str


class Message(BaseModel):
    message: str
