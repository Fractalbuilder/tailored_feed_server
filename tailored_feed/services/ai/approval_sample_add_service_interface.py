from abc import ABC, abstractmethod
from tailored_feed.models.ai.approval_sample import ApprovalSample

class ApprovalSampleAddServiceInterface(ABC):

    @abstractmethod
    def generate_iteration_model(
        self, get_repository, iteration: int, assessment_id: int, 
        question_index_assessed: int, assessment_last_question_index: int
    ):
        pass

    @abstractmethod
    def predict_student_approval(
        self, get_repository, add_repository, assessment_id, session_id, session_student_id,
        question_index_assessed, iteration, assessment_last_question_index
    ):
        pass