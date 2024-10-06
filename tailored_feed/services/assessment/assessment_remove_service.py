import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.repositories.common.db_repository import DbRepository
from tailored_feed.services.assessment.assessment_remove_service_interface import AssessmentRemoveServiceInterface

class AssessmentRemoveService(AssessmentRemoveServiceInterface):
    def __init__(self, remove_repository):
        self.exception_manager = ExceptionManager()
        self.db_repository = DbRepository()
        self.remove_repository = remove_repository

    def remove(self, assessment_id: int):
        try:
            self.remove_repository.remove(assessment_id=assessment_id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parametros, str(e))
    

    def remove_n_save(self, assessment_id: int):
        try:
            self.db_repository.start_transaction()
            self.remove(assessment_id=assessment_id)
            self.db_repository.save()
            self.db_repository.close_transaction()

        except Exception as e:
            self.db_repository.roll_back()
            argspec = inspect.getfullargspec(self.remove_n_save)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove_n_save", parametros, str(e))