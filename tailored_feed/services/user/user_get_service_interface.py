from abc import ABC, abstractmethod

class UserGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass