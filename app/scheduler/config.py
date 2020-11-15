import os

BACKEND_IP = os.environ["BACKEND_IP"]
TIME_TO_START = str(os.environ["TIME_TO_START"])
LINES_TO_ENABLE = [int(line) for line in str(os.environ["LINES_TO_ENABLE"]).split(',')]
CITY = os.environ["CITY"]
HOURS_AFTER_SUNSET = int(os.environ["HOURS_AFTER_SUNSET"])
USERS = [{"name": "Cottage", "id": os.environ["GROUP_CHAT_ID_COTTAGE"]}]
