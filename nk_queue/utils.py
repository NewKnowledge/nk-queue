from datetime import datetime


def current_timestamp():
    return int(datetime.timestamp(datetime.now()))


def future_timestamp():
    return int(datetime.timestamp(datetime.now())) + 55
