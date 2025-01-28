import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_get_repository_interface import QuestionGetRepositoryInterface

class QuestionGetRepository(QuestionGetRepositoryInterface):
    
    def __init__(self):
        self.exception_manager = ExceptionManager()


    def by_id(self, id: int):
        try:
            return AssessmentQuestion.objects.get(id=id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parameters, str(e))


    def by_assessment_id(self, assessment_id: int):
        try:
            question = AssessmentQuestion.objects.filter(assessment_id=assessment_id).order_by('id')
            return question

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_assessment_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_assessment_id", parameters, str(e))


    def by_index_and_assessment_id(self, index: int, assessment_id: int):
        try:
            return AssessmentQuestion.objects.get(index=index, assessment_id=assessment_id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_index_and_assessment_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_index_and_assessment_id", parameters, str(e))