from typing import Optional
import uuid
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: uuid.UUID
    username: str
    hashed_password: str
    disabled: bool
    is_admin: bool
    email: Optional[str] = None
    full_name: Optional[str] = None
