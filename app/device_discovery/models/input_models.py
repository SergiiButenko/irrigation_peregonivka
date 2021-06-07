from pydantic import BaseModel
from typing import Optional


class Operation(BaseModel):
    operation: str
