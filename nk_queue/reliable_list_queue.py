from collections import namedtuple
from uuid import uuid4

from nk_queue.list_queue import ListQueue, Message
from nk_queue.abstract_queue_client import AbstractQueueClient


class ReliableListQueue(ListQueue):
    def __init__(self, queue_name, queue_client: AbstractQueueClient, iterator_timeout=0):
        super().__init__(queue_name, queue_client, iterator_timeout)
        self._save_queue_name = f"{self._queue_name}_save_{uuid4()}"

    def __next__(self):
        saved_item = self._queue_client.read(self._save_queue_name)

        if saved_item:
            return Message(saved_item[0][1])

        item = self._queue_client.get_and_save(self._queue_name, self._save_queue_name, timeout=self._iterator_timeout)

        if item:
            return Message(item[1])
        else:
            raise StopIteration()

    def remove_saved_item(self, item):
        return self._queue_client.delete(self._save_queue_name, item)
