import os

from nk_queue.list_queue_client import ListQueueClient

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_delete():
    client = ListQueueClient(HOST, PORT, DB)

    try:
        client.delete()
    except Exception as e:
        assert isinstance(e, NotImplementedError)
