from abc import ABC, abstractmethod

class SessionStudentGetRepositoryInterface(ABC):

    @abstractmethod
    def by_session(self, session):
        pass

    @abstractmethod
    def by_session_n_user(self, session, user):
        pass