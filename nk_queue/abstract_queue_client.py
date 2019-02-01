from abc import ABC, abstractmethod


class AbstractQueueClient(ABC):

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
