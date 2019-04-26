import os

from nk_queue.sorted_queue_client import SortedQueueClient

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_delete():
    client = SortedQueueClient(HOST, PORT, DB)

    try:
        client.read()
    except Exception as e:
        assert isinstance(e, NotImplementedError)
