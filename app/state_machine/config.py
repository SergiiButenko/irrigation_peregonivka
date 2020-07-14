import os


BACKEND_IP = os.environ["BACKEND_IP"]
# Should be max+1 from max id from table
BRANCHES_LENGTH = 40
RULES_FOR_BRANCHES = [None] * BRANCHES_LENGTH
RAIN_HOURS = 12
RAIN_MAX = 1500  # mm per m^2
REDIS_KEY_FOR_MESSENGER = "telegram_sent_intervals"
MESSENGER_SENT_TIMEOUT = 10
LINE_UPPER_TANK = 26
LINES_UPPER_TANK = {"upper_tank": LINE_UPPER_TANK}
USERS = [{"name": "Cottage", "id": os.environ["GROUP_CHAT_ID_COTTAGE"]}]
WEBHOOK_URL_BASE = os.environ["WEBHOOK_URL_BASE"]
MAX_TIME_DELTA_FOR_RULES_SERVICE_MIN = 5
