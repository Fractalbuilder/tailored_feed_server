from abc import ABC, abstractmethod

class AssessmentRemoveServiceInterface(ABC):

    @abstractmethod
    def remove(self, assessment_id: int):
        pass

    @abstractmethod
    def remove_n_save(self, assessment_id: int):
        pass