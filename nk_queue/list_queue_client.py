import redis
from nk_queue.abstract_queue_client import AbstractQueueClient


class ListQueueClient(AbstractQueueClient):
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

    def get(self, queue_name, timeout=1):
        return self.operation_context().brpop(queue_name, timeout=timeout)

    def get_and_save(self, queue_name, destination_queue_name, timeout=1):
        return self.operation_context().brpoplpush(queue_name, destination_queue_name, timeout=timeout)

    def read(self, queue_name, start_index=-1, end_index=-1):
        return self.operation_context().lrange(queue_name, start_index, end_index)

    def delete(self, queue_name, item, count=0):
        return self.operation_context().lrem(queue_name, count, item)

    def put(self, queue_name, item):
        return self.operation_context().lpush(queue_name, item)

    def r_put(self, queue_name, item):
        return self.operation_context().rpush(queue_name, item)

    def list_all(self, queue_name):
        return self.operation_context().lrange(queue_name, 0, -1)
