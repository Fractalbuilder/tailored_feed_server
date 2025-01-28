from abc import ABC, abstractmethod

class UserGetRepositoryInterface(ABC):

    @abstractmethod
    def by_id(self, id: int):
        pass