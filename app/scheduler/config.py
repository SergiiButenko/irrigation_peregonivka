import os

BACKEND_IP = os.environ["BACKEND_IP"]
TIME_TO_START = str(os.environ["TIME_TO_START"])
LINES_TO_ENABLE = [int(line) for line in str(os.environ["LINES_TO_ENABLE"]).split(',')]