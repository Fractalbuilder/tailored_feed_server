import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.services.question.questions_arrange_service_interface import QuestionsArrangeServiceInterface

class QuestionsArrangeService(QuestionsArrangeServiceInterface):

    def __init__(self, get_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository


    def arrange(self, assessment_id: int):
        try:
            questions = self.get_repository.by_assessment_id(assessment_id)

            for index, question in enumerate(questions):
                question.index = index
                question.save()

        except Exception as e:
            argspec = inspect.getfullargspec(self.arrange)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "arrange", parameters, str(e))
