import uuid
from datetime import datetime

from pydantic import BaseModel


class DeviceSql(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    type: str
    version: str
    last_known_ip: str
    updated: datetime


class ComponentSql(BaseModel):
    id: uuid.UUID
    name: str
    device_id: str
    type: str
    version: str
    component_type: str


class Message(BaseModel):
    message: str
