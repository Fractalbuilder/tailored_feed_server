from abc import ABC, abstractmethod
from tailored_feed.models.ai.approval_sample import ApprovalSample

class ApprovalSampleAddServiceInterface(ABC):

    @abstractmethod
    def generate_iteration_model(
        self, iteration: int, assessment_id: int, session_student_id: int, session_id: int, 
        question_index_assessed: int, assessment_last_question_index: int
    ):
        pass

    @abstractmethod
    def predict_student_approval(
        self, assessment_id, session_id, session_student_id,
        iteration_index_assessed, iteration, assessment_last_question_index
    ):
        pass