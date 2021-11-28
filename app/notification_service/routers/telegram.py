from notification_service.schema.schema import TelegramMessage
from notification_service.service_providers.logger import logger
from fastapi.routing import APIRouter
from fastapi import status, Response
from notification_service.service_providers.telegram_bot import telegram_bot


router = APIRouter(
    prefix="/telegram/{user_id}",
    tags=["web sockets"],
)


@router.post(
    "/message",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def telegram_send(
    message: TelegramMessage,
    user_id: str,
):
    logger.info(f"Sending '{message}' to {user_id}")
    # telegram_bot.send_message(user_id, message)
