from typing import Optional
import uuid
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


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


class SensorValue(BaseModel):
    data: dict


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


class SensorSQL(BaseModel):
    id: int
    device_id: str
    name: str
    group_id: uuid.UUID
    category: str
    type: str
    version: str
    settings: Optional[dict] = None
