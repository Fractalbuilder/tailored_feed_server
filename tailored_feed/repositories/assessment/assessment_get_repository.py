import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.models.user import User
from tailored_feed.repositories.assessment.assessment_get_repository_interface import AssessmentGetRepositoryInterface

class AssessmentGetRepository(AssessmentGetRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()
        
    
    def by_id(self, id: int):
        try:
            return Assessment.objects.get(id=id)
        
        except ContentError as e:
            raise ContentError(str(e))

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parameters, str(e))


    def by_owner_id(self, owner_id: int):
        try:
            owner = User.objects.get(id=int(owner_id))

            if owner is None:
                raise ContentError('No se encontró el usuario vinculado a la evaluación')

            return Assessment.objects.filter(owner=owner).order_by('-id')
        
        except ContentError as e:
            raise ContentError(str(e))

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_owner_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_owner_id", parameters, str(e))


    def all(self):
        try:
            return Assessment.objects.all().order_by('-creationDate')
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.all)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "all", parameters, str(e))