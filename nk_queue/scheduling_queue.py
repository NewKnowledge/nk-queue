from nk_queue.abstract_queue_client import AbstractQueueClient
from nk_queue.utils import current_timestamp


class SchedulingQueue:
    def __init__(self, queue_name, queue_client: AbstractQueueClient):
        self._queue_name = queue_name
        self._queue_client = queue_client

    def initialize(self):
        self._queue_client.connect()

    def schedule_item(self, scheduled_timestamp, item):
        return self._queue_client.put(self._queue_name, scheduled_timestamp, item)

    def get_scheduled_items(self, with_scores=True):
        return self._queue_client.get(
            self._queue_name, max=current_timestamp(), with_scores=with_scores
        )

    def remove_item(self, item):
        return self._queue_client.delete(self._queue_name, item)

    def list_all(self, with_scores=True):
        return self._queue_client.list_all(self._queue_name, with_scores=with_scores)

    def begin_transaction(self):
        self._queue_client.begin_transaction()

    def commit_transaction(self):
        self._queue_client.commit_transaction()

    def abort_transaction(self):
        self._queue_client.abort_transaction()
