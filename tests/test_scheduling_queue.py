import os
from random import randint
import sys
import time

from nk_queue.scheduling_queue import SchedulingQueue
from nk_queue.sorted_queue_client import SortedQueueClient
from nk_queue.utils import current_timestamp

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_schedule_item():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1


def test_get_scheduled_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    time.sleep(1)

    get_output = queue.get_scheduled_items(with_scores=False)
    assert isinstance(get_output, list)
    assert get_output[0].decode("utf-8") == "test item"


def test_remove_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    time.sleep(1)

    output = queue.remove_item("test item")
    assert output == 1


def test_transaction_commit_schedule_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    queue.begin_transaction()
    queue.schedule_item(current_timestamp(), "test transaction item")
    queue.commit_transaction()

    time.sleep(1)

    get_output = queue.get_scheduled_items(with_scores=False)
    assert isinstance(get_output, list)
    assert len(get_output) == 2

    assert get_output[0].decode("utf-8") == "test item"
    assert get_output[1].decode("utf-8") == "test transaction item"


def test_transaction_commit_remove_schedule_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    queue.begin_transaction()
    queue.remove_item("test item")
    queue.commit_transaction()

    time.sleep(1)

    get_output = queue.get_scheduled_items(with_scores=False)
    assert isinstance(get_output, list)
    assert len(get_output) == 0


def test_transaction_abort_schedule_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    queue.begin_transaction()
    queue.schedule_item(current_timestamp(), "test transaction item")
    queue.abort_transaction()

    time.sleep(1)

    get_output = queue.get_scheduled_items(with_scores=False)
    assert isinstance(get_output, list)
    assert len(get_output) == 1
    assert get_output[0].decode("utf-8") == "test item"


def test_transaction_abort_remove_schedule_items():
    queue = SchedulingQueue(
        f"test_schedule_queue_{randint(0, 1000)}", SortedQueueClient(HOST, PORT, DB)
    )
    queue.initialize()
    output = queue.schedule_item(current_timestamp(), "test item")
    assert output == 1

    queue.begin_transaction()
    queue.remove_item("test item")
    queue.abort_transaction()

    time.sleep(1)

    get_output = queue.get_scheduled_items(with_scores=False)
    assert isinstance(get_output, list)
    assert len(get_output) == 1
    assert get_output[0].decode("utf-8") == "test item"
