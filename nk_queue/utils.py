from datetime import datetime


def current_timestamp():
    return int(datetime.timestamp(datetime.now()))


def timestamp(datetime):
    return int(datetime.timestamp(datetime))
