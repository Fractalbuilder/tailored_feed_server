import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_remove_repository_interface import QuestionRemoveRepositoryInterface

class QuestionRemoveRepository(QuestionRemoveRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def remove(self, id: int):
        try:
            question = AssessmentQuestion.objects.get(id=id)
            question.delete()

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parametros, str(e))