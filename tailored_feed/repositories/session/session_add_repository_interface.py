from abc import ABC, abstractmethod
from tailored_feed.models.session.session import Session

class SessionAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, session: Session):
        pass