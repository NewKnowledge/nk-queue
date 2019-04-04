from datetime import datetime
from random import randint


def current_timestamp():
    return int(datetime.timestamp(datetime.now()))


def future_timestamp():
    return int(datetime.timestamp(datetime.now())) + 55
