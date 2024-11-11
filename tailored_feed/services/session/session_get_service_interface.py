from abc import ABC, abstractmethod

class SessionGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass

    @abstractmethod
    def by_assessment_id(self, assessment_id):
        pass