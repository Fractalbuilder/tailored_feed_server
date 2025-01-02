from abc import ABC, abstractmethod

class SessionGetRepositoryInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass

    @abstractmethod
    def by_assessment_id(self, assessment_id):
        pass

    @abstractmethod
    def all_active(self):
        pass