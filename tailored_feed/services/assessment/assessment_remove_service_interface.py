from abc import ABC, abstractmethod

class AssessmentRemoveServiceInterface(ABC):

    @abstractmethod
    def remove(self, id: int):
        pass

    @abstractmethod
    def remove_n_save(self, id: int):
        pass