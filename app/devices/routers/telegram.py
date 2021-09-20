from devices.models.telegram import TelegramMessage
from fastapi import APIRouter, Depends

from devices.dependencies import get_logger, telegram_bot

router = APIRouter(
    prefix="/telegram/{user_id}/message",
    tags=["telegram"]
)


@router.post("", name="Get sensor model")
async def get_sensor(
    user_id: str,
    message: TelegramMessage,
    telegram_bot=Depends(telegram_bot),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Sending '{message}' to {user_id}")
    telegram_bot.send_message(user_id, message)

    return "OK"
