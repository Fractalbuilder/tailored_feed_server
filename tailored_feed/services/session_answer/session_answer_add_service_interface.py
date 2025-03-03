from abc import ABC, abstractmethod
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionAnswerAddServiceInterface(ABC):

    @abstractmethod
    def add(
        self, question_id: int, session_student, question_index, selected_options, user_context, start_date
    ):
        pass