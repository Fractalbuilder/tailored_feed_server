from abc import ABC, abstractmethod

class SessionStudentGetServiceInterface(ABC):

    @abstractmethod
    def by_session(self, session_id):
        pass

    @abstractmethod
    def by_session_with_students(self, session_id):
        pass

    @abstractmethod
    def by_session_n_user(self, session_id, student_id):
        pass

    @abstractmethod
    def get_avg_question_index(self, session_id, last_question_index):
        pass