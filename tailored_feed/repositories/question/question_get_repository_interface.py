from abc import ABC, abstractmethod

class QuestionGetRepositoryInterface(ABC):

    @abstractmethod
    def by_id(self, id: int):
        pass

    @abstractmethod
    def by_assessment_id(self, assessment_id: int):
        pass