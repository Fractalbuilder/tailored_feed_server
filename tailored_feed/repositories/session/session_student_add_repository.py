import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.session.session_add_repository_interface import SessionAddRepositoryInterface

class SessionStudentAddRepository(SessionStudentAddRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def add(self, session_student: SessionStudent):
        try:
            sessionStudent.save()

            return sessionStudent

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))