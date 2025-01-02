from abc import ABC, abstractmethod

class SessionAddServiceInterface(ABC):

    @abstractmethod
    def add(self, session_id: int, student_id: int):
        pass

    @abstractmethod
    def add_n_save(self, session_id: int, student_id: int):
        pass