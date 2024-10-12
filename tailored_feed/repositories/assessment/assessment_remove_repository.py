import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentRemoveRepository:

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def remove(self, assessment_id: int):
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            assessment.delete()

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parametros, str(e))