from abc import ABC, abstractmethod

class DbRepositoryInterface(ABC):

    @abstractmethod
    def start_transaction(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def roll_back(self):
        pass

    @abstractmethod
    def close_transaction(self):
        pass