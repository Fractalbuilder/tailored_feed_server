import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session import Session
from tailored_feed.services.session.session_add_service_interface import SessionAddServiceInterface

class SessionAddService(SessionAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def add(self, session: Session):
        try:
            return self.add_repository.add(session=session)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))
    

    def add_n_save(self, session: Session):
        try:
            session = self.add(session)
            return session
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parameters, str(e))