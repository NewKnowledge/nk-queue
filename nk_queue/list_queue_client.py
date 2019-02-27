import redis
from nk_queue.abstract_queue_client import AbstractQueueClient


class ListQueueClient(AbstractQueueClient):
    def __init__(self, host, port, db, auth_token=None):
        self._host = host
        self._port = port
        self._db = db
        self.auth_token = auth_token
        self._redis = None

    def connect(self):
        self._redis = redis.Redis(self._host, self._port, self._db, self.auth_token)

    def get(self, queue_name, timeout=1):
        return self._redis.brpop(queue_name, timeout=timeout)

    def put(self, queue_name, item):
        return self._redis.lpush(queue_name, item)

    def delete(self):
        raise NotImplementedError()
