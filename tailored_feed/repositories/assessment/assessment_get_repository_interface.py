from abc import ABC, abstractmethod

class AssessmentGetRepositoryInterface(ABC):

    @abstractmethod
    def all(self):
        pass