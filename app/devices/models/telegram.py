from pydantic import BaseModel, Field


class TelegramMessage(BaseModel):
    message: str
