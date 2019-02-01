import redis

from nk_queue.abstract_pub_sub_client import AbstractPubSubClient


class RedisPubSubClient(AbstractPubSubClient):
    def __init__(self, host, port, db, channel):
        self._host = host
        self._port = port
        self._db = db
        self._channel = channel
        self._redis = None
        self._pubsub = None

    def initialize(self):
        self._redis = redis.Redis(self._host, self._port, self._db)
        self._pubsub = self._redis.pubsub()
        self._pubsub.subscribe(self._channel)

    def publish(self, message):
        self._redis.publish(self._channel, message)

    def get_message(self):
        return self._pubsub.get_message()

