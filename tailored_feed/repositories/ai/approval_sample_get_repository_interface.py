from abc import ABC, abstractmethod

class ApprovalSampleGetRepositoryInterface(ABC):

    @abstractmethod
    def finished_session_students_answers(
        self, assessment_id, question_index_assessed, assessment_last_question_index
    ):
        pass

    @abstractmethod
    def finished_session_student_answers(
        self, session_student_id, question_index_assessed, assessment_last_question_index
    ):
        pass