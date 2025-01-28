from abc import ABC, abstractmethod

class QuestionGetServiceInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        pass

    @abstractmethod
    def by_assessment_id(self, assessment_id):
        pass

    @abstractmethod
    def by_index_and_assessment_id(self, index, assessment_id):
        pass