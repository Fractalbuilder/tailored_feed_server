from abc import ABC, abstractmethod

class AssessmentAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, name: str, owner: User):
        pass