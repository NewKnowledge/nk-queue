import redis


class Subscriber:
    def __init__(self, host, port, db, channel):
        self._host = host
        self._port = port
        self._db = db
        self._channel = channel
        self._redis = None
        self._pubsub = None

    def connect(self):
        self._redis = redis.Redis(self._host, self._port, self._db)
        self._pubsub = self._redis.pubsub()
        self._pubsub.subscribe(self._channel)

    def get_message(self):
        return self._pubsub.get_message()
