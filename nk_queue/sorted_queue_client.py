import redis
from nk_queue.abstract_queue_client import AbstractQueueClient
import sys


class SortedQueueClient(AbstractQueueClient):
    def __init__(self, host, port, db, auth_token=None, ssl=False):
        super().__init__()
        self._host = host
        self._port = port
        self._db = db
        self._auth_token = auth_token
        self._ssl = ssl

    def connect(self):
        self._redis = redis.Redis(
            host=self._host,
            port=self._port,
            db=self._db,
            password=self._auth_token,
            ssl=self._ssl,
        )

    def get(self, queue_name, min=0, max=sys.maxsize, with_scores=True):
        return self.operation_context().zrangebyscore(
            queue_name, min=min, max=max, withscores=with_scores
        )

    def read(self):
        raise NotImplementedError()

    def put(self, queue_name, scheduled_timestamp, item):
        return self.operation_context().zadd(queue_name, {item: scheduled_timestamp})

    def delete(self, queue_name, item):
        return self.operation_context().zrem(queue_name, item)

    def list_all(self, queue_name, with_scores=True):
        return self.operation_context().zrange(queue_name, 0, -1, withscores=with_scores)
