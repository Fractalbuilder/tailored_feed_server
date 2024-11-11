from abc import ABC, abstractmethod
from tailored_feed.models.session.session import Session

class SessionAddServiceInterface(ABC):

    @abstractmethod
    def add(self, session: Session):
        pass

    @abstractmethod
    def add_n_save(self, session: Session):
        pass