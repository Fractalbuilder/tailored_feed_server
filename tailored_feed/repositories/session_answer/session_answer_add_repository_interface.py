from abc import ABC, abstractmethod
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionAnswerAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, session_answer):
        pass