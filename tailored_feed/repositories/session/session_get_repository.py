import inspect
from django.db.models import Q
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.session.session_get_repository_interface import SessionGetRepositoryInterface

class SessionGetRepository(SessionGetRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def by_id(self, id):
        try:
            return Session.objects.get(id=id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parameters, str(e))
        
    
    def by_assessment_id(self, assessment_id):
        try:
            return Session.objects.filter(assessment_id=assessment_id).order_by('-id')
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_assessment_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_assessment_id", parameters, str(e))


    def all_active(self):
        try:
            return Session.objects.filter(
                Q(state="waiting") | Q(state="in_process")
            ).order_by('creationDate')
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.all_active)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "all_active", parameters, str(e))