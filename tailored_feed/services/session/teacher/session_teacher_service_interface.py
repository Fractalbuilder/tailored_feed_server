from abc import ABC, abstractmethod

class SessionTeacherServiceInterface(ABC):

    @abstractmethod
    def handle_state(self, session_id, new_state):
        pass

    @abstractmethod
    def start_session(self, session_id, assessment_id):
        pass

    @abstractmethod
    def end_session(self, session_id):
        pass