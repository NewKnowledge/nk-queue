from abc import ABC, abstractmethod


class AbstractPubSubClient(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def publish(self, message):
        pass

    @abstractmethod
    def get_message(self):
        pass
