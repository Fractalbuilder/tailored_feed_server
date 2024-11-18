from abc import ABC, abstractmethod
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentAddServiceInterface(ABC):

    @abstractmethod
    def add(self, assessment: Assessment):
        pass

    @abstractmethod
    def add_n_save(self, assessment: Assessment):
        pass