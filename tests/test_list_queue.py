import os
from random import randint

from redis.client import Pipeline
from nk_queue.list_queue import ListQueue
from nk_queue.list_queue_client import ListQueueClient

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_put():
    list_queue = ListQueue(f"test_list_queue_{randint(0, 1000)}", ListQueueClient(HOST, PORT, DB))
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
