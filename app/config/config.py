import os

########## TELEGRAM SETTINGS #############
if "API_TOKEN_MOZART" not in os.environ or "GROUP_CHAT_ID_COTTAGE" not in os.environ:
    raise AssertionError(
        "Please configure TELEBOT_BOT_TOKEN and GROUP_CHAT_ID as environment variables"
    )

API_TOKEN = os.getenv("API_TOKEN_MOZART", None)
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID_COTTAGE", -1))
NAME = "Peregonivka_bot"
CHANNEL_NAME = "@Butenko_test"

WEBHOOK_HOST = "mozz.breeze.ua"
WEBHOOK_PORT = 88  # 443, 80, 88 or 8443 (port needs to be open)
WEBHOOK_LISTEN = "0.0.0.0"  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = (
    "/var/www/app/ssl_sertificats/mozz/latest/cert.pem"
)  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = (
    "/var/www/app/ssl_sertificats/mozz/latest/privkey.pem"
)  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

MESSAGES = {"test": ""}

########## APP SETTINGS #############
LINE_UPPER_TANK = 26
LINE_UPPER_TANK_AV = 17
LINE_HEAT_SENSOR = 11
LINE_HEAT_HUN_SENSOR = 10

RAIN_HOURS = 12
RAIN_MAX = 1500  # mm per m^2
RAIN_CONSTANT_VOLUME = 0.73  # 8.2  ml per 120cm^2 -- 0.069 mm per m^2

TEMP_HOURS = 12
HEAT_ID = 12

MAX_DELTA_FOR_RULES_SERVICE = 5

START_RULE = 1
STOP_RULE = 2
ENABLED_RULE = 1


BACKEND_PORT = 8000
BACKEND_HOST = "192.168.71.113"
BACKEND_IP = "http://%s:%s" % (BACKEND_HOST, BACKEND_PORT)
VIBER_BOT_IP = WEBHOOK_URL_BASE

BRANCHES_LENGTH = 40
RULES_FOR_BRANCHES = [None] * BRANCHES_LENGTH
BRANCHES_SETTINGS = {}
APP_SETTINGS = {}

REDIS_KEY_FOR_UPPER_TANK = "UPPER_TANK"
REDIS_KEY_FOR_CESSTOOL = "CESSTOOL"
TANK_NOTIFICATION_MINUTES = 1
CESSTOOL_NOTIFICATION_MINUTES = 60 * 8
LINES_UPPER_TANK = {"upper_tank": LINE_UPPER_TANK, "upper_tank_sv": LINE_UPPER_TANK_AV}

READ_TIMEOUT = 10
RESP_TIMEOUT = 10

########## TELEGRAM SETTINGS #############

REDIS_KEY_FOR_VIBER = "telegram_sent_intervals"
VIBER_SENT_TIMEOUT = 10
USERS = [{"name": "Cottage", "id": "-315337397"}]

# Settings for upper tanks
USERS_SV = [{"name": "SV", "id": "cHxBN+Zz1Ldd/60xd62U/w=="}]
TELEGRAM_USERS = {
     "upper_tank": USERS,
     "cesspool": USERS,
     "upper_tank_sv": USERS_SV
     }

VIBER_USERS = [
    {"name": "Sergii", "id": "cHxBN+Zz1Ldd/60xd62U/w=="},
    {"name": "Oleg", "id": "IRYaSCRnmV1IT1ddtB8Bdw=="},
    {"name": "Irina", "id": "mSR74mGibK+ETvTTx2VvcQ=="},
]
