from abc import ABC, abstractmethod
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion

class QuestionAddServiceInterface(ABC):

    @abstractmethod
    def add(self, question: AssessmentQuestion):
        pass

    @abstractmethod
    def add_n_save(self, question: AssessmentQuestion):
        pass