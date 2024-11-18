import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.services.question.question_remove_service_interface import QuestionRemoveServiceInterface

class QuestionRemoveService(QuestionRemoveServiceInterface):
    def __init__(self, remove_repository, assessment_add_service):
        self.exception_manager = ExceptionManager()
        self.remove_repository = remove_repository
        self.assessment_add_service = assessment_add_service


    def remove(self, id: int):
        try:
            self.remove_repository.remove(id=id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parameters, str(e))
    

    def remove_n_save(self, id: int, assessment: Assessment):
        try:
            self.remove(id=id)
            assessment.totalQuestions = assessment.totalQuestions - 1
            self.assessment_add_service.add_n_save(assessment)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove_n_save)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove_n_save", parameters, str(e))