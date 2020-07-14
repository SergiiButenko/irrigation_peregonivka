import os

BACKEND_IP = os.environ["BACKEND_IP"]
USERS = [{"name": "Cottage", "id": os.environ["GROUP_CHAT_ID_COTTAGE"]}]
REDIS_KEY_FOR_MESSENGER = "telegram_sent_intervals"
MESSENGER_SENT_TIMEOUT = 10
WEBHOOK_URL_BASE = os.environ["WEBHOOK_URL_BASE"]
HEAT_ID = 12
RESTART_INTERVAL_MIN = int(os.environ["RESTART_INTERVAL_MIN"]) * 60