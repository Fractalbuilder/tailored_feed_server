import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.services.assessment.assessment_add_service_interface import AssessmentAddServiceInterface

class AssessmentAddService(AssessmentAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def add(self, assessment: Assessment):
        try:
            return self.add_repository.add(assessment)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))
    

    def add_n_save(self, assessment: Assessment):
        try:
            assessment = self.add(assessment)
            assessment_dict = assessment.to_dict()

            return assessment_dict
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parameters, str(e))