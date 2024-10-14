import inspect
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_get_repository_interface import QuestionGetRepositoryInterface

class QuestionGetRepository(QuestionGetRepositoryInterface):
    
    def by_id(self, id: int):
        try:
            return AssessmentQuestion.objects.get(id=id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parametros, str(e))


    def by_assessment_id(self, assessment_id: int):
        try:
            return AssessmentQuestion.objects.filter(assessment_id=assessment_id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_assessment_id)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_assessment_id", parametros, str(e))