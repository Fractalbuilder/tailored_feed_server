from abc import ABC, abstractmethod
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionStudentAddServiceInterface(ABC):

    @abstractmethod
    def create_or_update_session_student(self, session, student, is_correct, current_question_index):
        pass

    @abstractmethod
    def grade_session_students(self, session_id):
        pass

    @abstractmethod
    def grade_student(self, session_id, student_id):
        pass