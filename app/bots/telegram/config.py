import os

API_TOKEN = os.environ["API_TOKEN_MOZART"]
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
WEBHOOK_URL_BASE_PUBLIC = os.environ["WEBHOOK_URL_BASE_PUBLIC"]