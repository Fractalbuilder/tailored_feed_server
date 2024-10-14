import inspect
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.repositories.assessment.assessment_get_repository_interface import AssessmentGetRepositoryInterface

class AssessmentGetRepository(AssessmentGetRepositoryInterface):
    
    def by_id(self, id):
        try:
            return Assessment.objects.get(id=id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parametros, str(e))


    def all(self):
        try:
            return Assessment.objects.all().order_by('-creationDate')
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.all)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "all", parametros, str(e))