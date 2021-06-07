import psycopg2
import psycopg2.extras
from actuator.config.config import DATABASE_CONNECTION_STR


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Postgres(metaclass=MetaSingleton):
    def __init__(self, db="mydb", user="postgres"):
        self.conn = psycopg2.connect(DATABASE_CONNECTION_STR)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
