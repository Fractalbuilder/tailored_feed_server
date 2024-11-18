from abc import ABC, abstractmethod
from tailored_feed.models.assessment.assessment import Assessment

class QuestionRemoveServiceInterface(ABC):

    @abstractmethod
    def remove(self, id: int):
        pass

    @abstractmethod
    def remove_n_save(self, id: int, assessment: Assessment):
        pass