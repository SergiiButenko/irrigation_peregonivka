from pydantic import BaseModel


class State(BaseModel):
    expected_state: str


class ActuatorSQL(BaseModel):
    id: str
    name: str
    device_id: str
    settings: dict

