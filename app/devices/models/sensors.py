from pydantic import BaseModel


class SensorValue(BaseModel):
    data: dict


class SensorSQL(BaseModel):
    id: str
    name: str
    device_id: str
