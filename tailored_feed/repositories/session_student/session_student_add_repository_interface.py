from abc import ABC, abstractmethod
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionStudentAddRepositoryInterface(ABC):

    @abstractmethod
    def create_or_update(self, session, student, is_correct, current_question_index):
        pass