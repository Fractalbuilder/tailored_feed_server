from abc import ABC, abstractmethod

class AssessmentRemoveRepositoryInterface(ABC):

    @abstractmethod
    def remove(self, id: int):
        pass