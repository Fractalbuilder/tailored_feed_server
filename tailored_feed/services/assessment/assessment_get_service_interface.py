from abc import ABC, abstractmethod

class AssessmentGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, assessment_id):
        pass

    @abstractmethod
    def all(self):
        pass