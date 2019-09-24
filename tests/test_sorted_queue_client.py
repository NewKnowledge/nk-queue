import os

from nk_queue.sorted_queue_client import SortedQueueClient
from nk_queue.utils import current_timestamp, future_timestamp

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_delete():
    client = SortedQueueClient(HOST, PORT, DB)

    try:
        client.read()
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_get_range():
    queue_name = "test_get_range_queue"
    sorted_queue_client = SortedQueueClient(HOST, PORT, DB)
    sorted_queue_client.connect()

    first_score = current_timestamp()
    second_score = current_timestamp()
    third_score = current_timestamp()

    sorted_queue_client.put(queue_name, first_score, "item1")
    sorted_queue_client.put(queue_name, second_score, "item2")
    sorted_queue_client.put(queue_name, third_score, "item3")

    # Passing no range values retrieves single item with greatest score.
    range_output = sorted_queue_client.get_range(queue_name, with_scores=False)

    assert isinstance(range_output, list)
    assert len(range_output) == 1
    assert range_output[0].decode("utf-8") == "item3"

    # Assert passing start / end range values retrieves expected items.
    range_output = sorted_queue_client.get_range(queue_name, start=0, end=1, with_scores=False)

    assert isinstance(range_output, list)
    assert len(range_output) == 2
    assert range_output[0].decode("utf-8") == "item3"
    assert range_output[1].decode("utf-8") == "item2"


def get_max_items():
    queue_name = "get_max_items_queue"
    sorted_queue_client = SortedQueueClient(HOST, PORT, DB)
    sorted_queue_client.connect()

    first_score = current_timestamp()
    second_score = current_timestamp()

    sorted_queue_client.put(queue_name, first_score, "item1")
    sorted_queue_client.put(queue_name, second_score, "item2")

    range_output = sorted_queue_client.get_max_items(queue_name, 1)

    assert isinstance(range_output, list)
    assert len(range_output) == 1
    assert range_output[0][0].decode("utf-8") == "item2"
