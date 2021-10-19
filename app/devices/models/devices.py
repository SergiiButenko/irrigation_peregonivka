from typing import List, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class DeviceSql(BaseModel):
    id: str
    description: str
    type: str
    version: str
    last_known_ip: Optional[str] = None
    updated: Optional[datetime] = None


class ComponentSql(BaseModel):
    id: uuid.UUID
    device_id: str
    component_id: int
    name: str
    category: str
    type: str
    version: str
    usage_type: Optional[str] = None
    settings: Optional[dict] = None
    telegram_notify: bool


class ComponentsSql(BaseModel):
    __root__: List[ComponentSql]


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class SensorValueNSQL(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    device_id: str
    sensor_id: int
    data: dict
    date: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class TelegramUser(BaseModel):
    id: str = Field(alias='telegram_user')
