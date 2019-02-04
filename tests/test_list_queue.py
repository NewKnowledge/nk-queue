import os
from nk_queue.list_queue import ListQueue
from nk_queue.list_queue_client import ListQueueClient
from random import randint

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_put():
    list_queue = ListQueue(f"test{randint(0, 1000)}", ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()
    output = list_queue.put("test")
    assert output == 1


def test_get():
    list_queue = ListQueue(f"test{randint(0, 1000)}", ListQueueClient(HOST, PORT, DB))
    list_queue.initialize()
    output = list_queue.put("test")
    assert output == 1

    get_output = list_queue.get()
    assert get_output.decode("utf-8") == "test"
