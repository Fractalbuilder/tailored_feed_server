import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.user import User
from tailored_feed.services.assessment.assessment_get_service_interface import AssessmentGetServiceInterface

class AssessmentGetService(AssessmentGetServiceInterface):
    def __init__(self, get_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository

    def all(self):
        try:
            return self.get_repository.all()

        except Exception as e:
            argspec = inspect.getfullargspec(self.all)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "all", parametros, str(e))
