import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.repositories.common.db_repository import DbRepository
from tailored_feed.models.user import User
from tailored_feed.services.assessment.assessment_add_service_interface import AssessmentAddServiceInterface

class AssessmentAddService(AssessmentAddServiceInterface):
    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.db_repository = DbRepository()
        self.add_repository = add_repository

    def add(self, name: str, owner: User):
        try:
            return self.add_repository.add(name=name, owner=owner)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parametros, str(e))
    

    def add_n_save(self, name: str, owner: User):
        try:
            self.db_repository.start_transaction()
            assessment = self.add(name=name, owner=owner)
            self.db_repository.save()
            assessment_dict = assessment.to_dict()
            self.db_repository.close_transaction()

            return assessment_dict

        except Exception as e:
            self.db_repository.roll_back()
            argspec = inspect.getfullargspec(self.add_n_save)
            parametros = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parametros, str(e))