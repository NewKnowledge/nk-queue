from nk_queue.abstract_queue_client import AbstractQueueClient


class ListQueue:
    def __init__(self, queue_name, queue_client: AbstractQueueClient):
        self._queue_name = queue_name
        self._queue_client = queue_client

    def initialize(self):
        self._queue_client.connect()

    def put(self, item):
        return self._queue_client.put(self._queue_name, item)

    def get(self):
        return self._queue_client.get(self._queue_name)

    def begin_transaction(self):
        self._queue_client.begin_transaction()

    def commit_transaction(self):
        self._queue_client.commit_transaction()

    def abort_transaction(self):
        self._queue_client.abort_transaction()
