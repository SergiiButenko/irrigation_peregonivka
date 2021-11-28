from devices.service_providers.httpx_client import HttpxClient
from devices.config.config import Config


class NotificationServiceClient:
    async def send_telegram_message(
        self, message, user=Config.TELEGRAM_CHAT_ID_COTTAGE
    ):
        return await HttpxClient.post_with_raise(
            url=f"{Config.NOTIFICATION_SERVICE_URL}/telegram/{user}/message",
            json={"message": message},
            headers=self.headers,
        )

    async def send_ws_message(self, message):
        return await HttpxClient.post_with_raise(
            url=f"{Config.NOTIFICATION_SERVICE_URL}/ws/message",
            json={"message": message},
            headers=self.headers,
        )