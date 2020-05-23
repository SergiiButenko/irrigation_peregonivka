import json
import logging

import redis
from app.helpers import *
from app.config import *

redis_db = redis.Redis(host="localhost", port=6379, db=0)

def set_next_rule_to_redis(branch_id, data):
    """Set next rule in redis."""
    res = False
    try:
        data = json.dumps(data, default=date_handler)
        res = redis_db.set(branch_id, data)
    except Exception as e:
        logging.error("Can't save data to redis. Exception occured {0}".format(e))

    return res


def get_next_rule_from_redis(branch_id):
    """Get next rule from redis."""
    json_to_data = None
    try:
        data = redis_db.get(branch_id)
        if data is None:
            return None

        json_to_data = json.loads(data.decode("utf-8"), object_hook=date_hook)
    except Exception as e:
        logging.error("Can't get data from redis. Exception occured {0}".format(e))

    return json_to_data


def get_time_last_notification(key=REDIS_KEY_FOR_UPPER_TANK):
    """"""
    data = None
    try:
        data = redis_db.get(key)
        if data is None:
            raise AssertionError("No value in {0} key in reddis db".format(key))

        return convert_to_datetime(data.decode("utf-8"))
    except Exception as e:
        logging.error("Can't get data from redis. Exception occured {0}".format(e))
        return None


def set_time_last_notification(
    key=REDIS_KEY_FOR_UPPER_TANK, date=datetime.datetime.now()
):
    """Set next rule in redis."""
    res = False
    try:
        date = date_handler(date)
        res = redis_db.set(key, date)
    except Exception as e:
        logging.error("Can't save date to redis. Exception occured {0}".format(e))

    return res


def flush_on_start():
    redis_db.flushdb()
