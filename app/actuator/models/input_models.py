from pydantic import BaseModel
from typing import Optional


class State(BaseModel):
    expected_state: str


class Operation(BaseModel):
    operation: str
