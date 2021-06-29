from pydantic import BaseModel


class Operation(BaseModel):
    operation: str
