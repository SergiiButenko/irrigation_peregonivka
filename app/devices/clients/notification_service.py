from devices.service_providers.httpx_client import HttpxClient
from devices.config.config import Config
from fastapi.encoders import jsonable_encoder

class NotificationServiceClient:
    async def send_telegram_message(
        self, message, user=Config.TELEGRAM_CHAT_ID_COTTAGE
    ):
        return await HttpxClient.post_with_raise(
            url=f"{Config.NOTIFICATION_SERVICE_URL}/telegram/{user}/message",
            json={"message": message},
        )

    async def send_ws_message(self, action, payload):
        return await HttpxClient.post(
            url=f"{Config.NOTIFICATION_SERVICE_URL}/ws/message",
            json={"action": action, "payload": jsonable_encoder(payload)},
        )


notification_service_client = NotificationServiceClient()
