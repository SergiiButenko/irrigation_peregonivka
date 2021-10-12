from devices.schemas.schema import TelegramMessage
from fastapi import APIRouter, Depends

from devices.dependencies import get_current_active_user, get_logger, get_telegram_bot

router = APIRouter(
    prefix="/telegram/{user_id}/message",
    tags=["telegram"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("", name="Send message to telegram")
async def send_message(
    user_id: str,
    message: TelegramMessage,
    telegram_bot=Depends(get_telegram_bot),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Sending '{message}' to {user_id}")
    # telegram_bot.send_message(user_id, message)

    return "OK"
