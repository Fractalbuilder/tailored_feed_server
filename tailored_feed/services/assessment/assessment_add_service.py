import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.user import User
from tailored_feed.services.assessment.assessment_add_service_interface import AssessmentAddServiceInterface

class AssessmentAddService(AssessmentAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def add(self, name: str, owner: User):
        try:
            return self.add_repository.add(name=name, owner=owner)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parametros, str(e))
    

    def add_n_save(self, name: str, owner: User):
        try:
            assessment = self.add(name=name, owner=owner)
            assessment_dict = assessment.to_dict()

            return assessment_dict
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parametros, str(e))