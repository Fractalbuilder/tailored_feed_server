from abc import ABC, abstractmethod

class AssessmentGetServiceInterface(ABC):

    @abstractmethod
    def all(self):
        pass