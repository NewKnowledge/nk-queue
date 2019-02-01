from nk_queue.abstract_pub_sub_client import AbstractPubSubClient


class Publisher:
    def __init__(self, client: AbstractPubSubClient):
        self._client = client

    def initialize(self):
        self._client.initialize()

    def broadcast_message(self, item):
        return self._client.publish(item)
