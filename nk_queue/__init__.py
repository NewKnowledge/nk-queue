from nk_queue.config import HOST, PORT, DB

from nk_queue.list_queue_client import ListQueueClient
from nk_queue.sorted_queue_client import SortedQueueClient

from nk_queue.list_queue import ListQueue
from nk_queue.scheduling_queue import SchedulingQueue


def get_queue(queue_type, queue_name, host=HOST, port=PORT, auth_token=None, ssl=False):
    host = HOST if host is None else host
    port = PORT if port is None else port
    auth_token = None if auth_token is None else auth_token

    if queue_type == "list":
        return ListQueue(queue_name, ListQueueClient(host, port, DB, auth_token, ssl))
    elif queue_type == "sorted":
        return SchedulingQueue(queue_name, SortedQueueClient(host, port, DB, auth_token, ssl))
    else:
        raise ModuleNotFoundError(
            f"{queue_type} is not a valid queue type, options include 'list', 'sorted'"
        )
