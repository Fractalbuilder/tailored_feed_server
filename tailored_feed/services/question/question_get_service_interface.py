from abc import ABC, abstractmethod

class QuestionGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass

    @abstractmethod
    def by_assessment_id(self, assessment_id):
        pass