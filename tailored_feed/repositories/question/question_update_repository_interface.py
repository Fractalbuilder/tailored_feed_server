from abc import ABC, abstractmethod
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion

class QuestionUpdateRepositoryInterface(ABC):

    @abstractmethod
    def update(self, question: AssessmentQuestion):
        pass