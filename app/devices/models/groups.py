from typing import List, Optional
import uuid
from pydantic import BaseModel


class Group(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    user_id: uuid.UUID


class Groups(BaseModel):
    __root__: List[Group]