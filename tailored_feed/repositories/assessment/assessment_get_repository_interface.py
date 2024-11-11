from abc import ABC, abstractmethod

class AssessmentGetRepositoryInterface(ABC):

    @abstractmethod
    def by_id(self, id: int):
        pass

    @abstractmethod
    def by_owner_id(self, owner_id: int):
        pass

    @abstractmethod
    def all(self):
        pass