from unittest.mock import MagicMock

from nk_queue.subscriber import Subscriber
from nk_queue.redis_pub_sub_client import RedisPubSubClient


def test_broadcast_message():
    redis_client = RedisPubSubClient('host', 'port', 'db', 'channel')
    redis_client.get_message = MagicMock(return_value='test_message')
    subscriber = Subscriber(redis_client)
    result = subscriber.get_message()

    redis_client.get_message.assert_called()
    assert result == 'test_message'
