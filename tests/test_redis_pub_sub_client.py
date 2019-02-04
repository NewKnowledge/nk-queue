import os

from nk_queue.redis_pub_sub_client import RedisPubSubClient
from nk_queue.subscriber import Subscriber
from nk_queue.publisher import Publisher

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")


def test_publish_and_subscriber():
    subscriber = Subscriber(RedisPubSubClient(HOST, PORT, DB, "test_channel"))
    subscriber.initialize()

    publisher = Publisher(RedisPubSubClient(HOST, PORT, DB, "test_channel"))
    publisher.initialize()

    publisher.publish("message")
    message = subscriber.get_message()

    assert message == {
        "channel": b"test_channel",
        "data": 1,
        "pattern": None,
        "type": "subscribe",
    }
