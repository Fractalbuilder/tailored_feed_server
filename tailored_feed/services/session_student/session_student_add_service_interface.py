from abc import ABC, abstractmethod
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionStudentAddServiceInterface(ABC):

    @abstractmethod
    def create_or_update_session_student(self, session, student, approved_questions, failed_questions, current_question_index):
        pass