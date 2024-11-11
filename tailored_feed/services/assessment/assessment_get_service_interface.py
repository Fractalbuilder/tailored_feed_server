from abc import ABC, abstractmethod

class AssessmentGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass

    @abstractmethod
    def by_owner_id(self, user_id):
        pass

    @abstractmethod
    def all(self):
        pass