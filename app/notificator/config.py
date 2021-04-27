import os

BACKEND_IP = os.environ["BACKEND_IP"]
RESTART_INTERVAL_MIN = int(os.environ["RESTART_INTERVAL_MIN"]) * 60
USERS = [{"name": "Cottage", "id": os.environ["GROUP_CHAT_ID_COTTAGE"]}]
WEBHOOK_URL_BASE = os.environ["WEBHOOK_URL_BASE"]
