from datetime import datetime


def current_timestamp():
    return int(datetime.timestamp(datetime.now()))


def future_timestamp():
    return int(datetime.timestamp(datetime.now())) + 55


def to_timestamp(datetime_object):
    return int(datetime.timestamp(datetime_object))


def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)
