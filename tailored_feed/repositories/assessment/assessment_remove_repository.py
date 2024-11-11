import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.repositories.assessment.assessment_remove_repository_interface import AssessmentRemoveRepositoryInterface

class AssessmentRemoveRepository(AssessmentRemoveRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def remove(self, id: int):
        try:
            assessment = Assessment.objects.get(id=id)
            assessment.delete()

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parameters, str(e))