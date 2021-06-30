from pydantic import BaseModel


class SensorValue(BaseModel):
    data: object
