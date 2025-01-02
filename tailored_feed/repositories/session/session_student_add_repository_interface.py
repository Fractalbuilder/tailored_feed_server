from abc import ABC, abstractmethod
from tailored_feed.models.session.session_student import SessionStudent

class SessionStudentAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, session_student: SessionStudent):
        pass