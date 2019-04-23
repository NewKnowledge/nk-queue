import os
from random import randint

from nk_queue.list_queue import ListQueue, Message
from nk_queue.list_queue_client import ListQueueClient

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_put():
    list_queue = ListQueue(
        f"test_list_queue_{randint(0, 1000)}", ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()
    output = list_queue.put("test")
    assert output == 1


def test_get():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()
    output = list_queue.put("test")
    assert output == 1

    get_output = list_queue.get()

    assert isinstance(get_output, tuple)

    # Queue name as first tuple item
    assert get_output[0].decode("utf-8") == queue_name

    # Queue value as second tuple item
    assert get_output[1].decode("utf-8") == "test"


def test_iterator():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    output = list_queue.put("test")
    assert output == 1

    for message in list_queue:
        assert isinstance(message, Message)

        # Queue name as first tuple item
        assert message.value.decode("utf-8") == "test"

        break


def test_transaction_commit():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()
    list_queue.begin_transaction()

    list_queue.put("test")

    list_queue.commit_transaction()

    get_output = list_queue.get()

    assert isinstance(get_output, tuple)

    # Queue name as first tuple item
    assert get_output[0].decode("utf-8") == queue_name

    # Queue value as second tuple item
    assert get_output[1].decode("utf-8") == "test"


def test_transaction_abort():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    list_queue.begin_transaction()
    list_queue.put("test")
    list_queue.abort_transaction()

    get_output = list_queue.get()

    assert get_output is None


def test_transaction_abort_with_previous_put():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    list_queue.put("test_prev")

    list_queue.begin_transaction()
    list_queue.put("test")
    list_queue.abort_transaction()

    get_output = list_queue.get()

    assert isinstance(get_output, tuple)

    # Queue name as first tuple item
    assert get_output[0].decode("utf-8") == queue_name

    # Queue value as second tuple item
    assert get_output[1].decode("utf-8") == "test_prev"

    next_get_output = list_queue.get()

    assert next_get_output is None


def test_delete():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    output = list_queue.put("test")
    assert output == 1

    output = list_queue.remove_item("test")

    assert output == 1


def test_list_all():
    queue_name = f"test_list_queue_{randint(0, 1000)}"
    list_queue = ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()

    list_queue.put("test")
    list_queue.put("test2")
    list_queue.put("test3")
    list_queue.put("test4")

    output = list_queue.list_all()

    assert len(output) == 4
    assert isinstance(output, list)
