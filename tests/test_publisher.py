from unittest.mock import MagicMock

from nk_queue.publisher import Publisher
from nk_queue.redis_pub_sub_client import RedisPubSubClient


def test_broadcast_message():
    redis_client = RedisPubSubClient('host', 'port', 'db', 'channel')
    redis_client.publish = MagicMock(return_value=1)
    publisher = Publisher(redis_client)
    result = publisher.broadcast_message('message')

    redis_client.publish.assert_called()
    assert result == 1
