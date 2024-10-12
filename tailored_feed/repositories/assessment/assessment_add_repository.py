import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentAddRepository:

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def add(self, name, owner):
        try:
            assessment = Assessment(name=name, owner=owner)
            assessment.save()

            return assessment

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parametros, str(e))