import os

BACKEND_IP = os.environ["BACKEND_IP"]
TIME_TO_RUN_SCHEDULER = str(os.environ["TIME_TO_RUN_SCHEDULER"])
CITY = os.environ["CITY"]
HOURS_AFTER_SUNSET = int(os.environ["HOURS_AFTER_SUNSET"])
USERS = [{"name": "Cottage", "id": os.environ["GROUP_CHAT_ID_COTTAGE"]}]
SCHEDULER_DEBUG_MODE = bool(
    int(os.environ.get("SCHEDULER_DEBUG_MODE", 0))
    )
WEBHOOK_URL_BASE = os.environ["WEBHOOK_URL_BASE"]
