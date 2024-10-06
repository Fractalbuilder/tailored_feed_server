from abc import ABC, abstractmethod

class AssessmentRemoveRepositoryInterface(ABC):

    @abstractmethod
    def remove(self, assessment_id: int):
        pass