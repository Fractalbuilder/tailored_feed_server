import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.services.assessment.assessment_remove_service_interface import AssessmentRemoveServiceInterface

class AssessmentRemoveService(AssessmentRemoveServiceInterface):
    def __init__(self, remove_repository):
        self.exception_manager = ExceptionManager()
        self.remove_repository = remove_repository

    def remove(self, assessment_id: int):
        try:
            self.remove_repository.remove(assessment_id=assessment_id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parametros, str(e))
    

    def remove_n_save(self, assessment_id: int):
        try:
            self.remove(assessment_id=assessment_id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove_n_save)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove_n_save", parametros, str(e))