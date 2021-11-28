from pydantic import BaseModel


class WSMessage(BaseModel):
    action: str
    payload: dict


class TelegramMessage(BaseModel):
    message: str
