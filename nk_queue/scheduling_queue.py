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

    def remove_items(self, from_timestamp, to_timestamp):
        return self._queue_client.delete(
            self._queue_name, min=from_timestamp, max=to_timestamp
        )
