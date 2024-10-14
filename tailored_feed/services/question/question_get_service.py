import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.services.question.question_get_service_interface import QuestionGetServiceInterface

class QuestionGetService(QuestionGetServiceInterface):

    def __init__(self, get_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository


    def by_id(self, id):
        try:
            return self.get_repository.by_id(id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parametros, str(e))


    def by_assessment_id(self, assessment_id):
        try:
            return self.get_repository.by_assessment_id(assessment_id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_assessment_id)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_assessment_id", parametros, str(e))
