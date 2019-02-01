from nk_queue.config import HOST, PORT, DB

from nk_queue.list_queue_client import ListQueueClient
from nk_queue.sorted_queue_client import SortedQueueClient

from nk_queue.list_queue import ListQueue
from nk_queue.scheduling_queue import SchedulingQueue

from nk_queue.redis_pub_sub_client import RedisPubSubClient
from nk_queue.publisher import Publisher
from nk_queue.subscriber import Subscriber


def get_queue(queue_type, queue_name):
    if queue_type == "list":
        return ListQueue(queue_name, ListQueueClient(HOST, PORT, DB))
    elif queue_type == "sorted":
        return SchedulingQueue(queue_name, SortedQueueClient(HOST, PORT, DB))
    else:
        raise ModuleNotFoundError(
            f"{queue_type} is not a valid queue type, options include 'list', 'sorted', 'pubsub'"
        )


def get_publisher(channel_name):
    return Publisher(RedisPubSubClient(HOST, PORT, DB, channel_name))


def get_subscriber(channel_name):
    return Subscriber(RedisPubSubClient(HOST, PORT, DB, channel_name))
