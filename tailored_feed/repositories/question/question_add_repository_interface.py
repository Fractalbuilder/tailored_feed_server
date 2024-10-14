from abc import ABC, abstractmethod
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion

class QuestionAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, question: AssessmentQuestion):
        pass