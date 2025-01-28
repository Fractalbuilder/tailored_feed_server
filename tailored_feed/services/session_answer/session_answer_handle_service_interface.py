from abc import ABC, abstractmethod

class SessionAnswerHandleServiceInterface(ABC):

    @abstractmethod
    def handle(
        self, assessment_question_id: int, selected_options, session_id: int, student_id: int,
        approved_questions: int, failed_questions: int, current_question_index: int
    ):
        pass