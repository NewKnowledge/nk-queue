from abc import ABC, abstractmethod


class AbstractQueueClient(ABC):
    def __init__(self):
        self._redis = None
        self._transaction = None

    def operation_context(self):
        return self._redis if not self.__has_transaction else self._transaction

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abstractmethod
    def list_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass

    @abstractmethod
    def r_put(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    def begin_transaction(self):
        if not self.__has_transaction:
            self._transaction = self._redis.pipeline()

        return self

    def commit_transaction(self):
        if self.__has_transaction:
            current_transaction = self._transaction
            self._transaction = None
            return current_transaction.execute()

    def abort_transaction(self):
        if self.__has_transaction:
            self._transaction.reset()
            self._transaction = None

    @property
    def __has_transaction(self):
        return self._transaction is not None
