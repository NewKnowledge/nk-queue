from nk_queue.abstract_pub_sub_client import AbstractPubSubClient


class Subscriber:
    def __init__(self, client: AbstractPubSubClient):
        self._client = client

    def initialize(self):
        self._client.initialize()

    def get_message(self):
        return self._client.get_message()
