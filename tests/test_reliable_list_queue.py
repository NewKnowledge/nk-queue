import os
from uuid import uuid4

from nk_queue.reliable_list_queue import ReliableListQueue
from nk_queue.list_queue import Message
from nk_queue.list_queue_client import ListQueueClient

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_reliable_list_queue():
    queue_name = f"test_reliable_list_queue_test_iterator"
    save_queue_name = f"test_reliable_list_queue_test_iterator_save"
    list_queue = ReliableListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    output = list_queue.put("test1")
    assert output == 1

    for message in list_queue:
        assert isinstance(message, Message)
        message_value = message.value.decode("utf-8")
        assert message_value == "test1"
        break

    item = list_queue._queue_client.get(save_queue_name)
    message_value = item.value.decode("utf-8")
    assert message_value == "test1"

    result = list_queue.remove_saved_item("test1")
    assert result == 1
