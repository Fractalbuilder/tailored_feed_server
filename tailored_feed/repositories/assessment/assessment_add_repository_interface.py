from abc import ABC, abstractmethod
from tailored_feed.models.user import User

class AssessmentAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, assessment: Assessment):
        pass