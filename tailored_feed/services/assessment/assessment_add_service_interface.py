from abc import ABC, abstractmethod
from tailored_feed.models.user import User

class AssessmentAddServiceInterface(ABC):

    @abstractmethod
    def add(self, name: str, owner: User):
        pass

    @abstractmethod
    def add_n_save(self, name: str, owner: User):
        pass