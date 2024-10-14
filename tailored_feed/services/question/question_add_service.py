import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.services.question.question_add_service_interface import QuestionAddServiceInterface

class QuestionAddService(QuestionAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def add(self, question: AssessmentQuestion):
        try:
            return self.add_repository.add(question)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parametros, str(e))
    

    def add_n_save(self, question: AssessmentQuestion):
        try:
            question = self.add(question)
            question_dict = question.to_dict()

            return question_dict
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parametros, str(e))