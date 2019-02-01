import redis


class Publisher:
    def __init__(self, host, port, db, channel):
        self._host = host
        self._port = port
        self._db = db
        self._channel = channel
        self._redis = None

    def initialize(self):
        self._redis = redis.Redis(self._host, self._port, self._db)

    def broadcast_message(self):
        self._redis.publish(self._channel, item)
