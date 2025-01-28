import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.user import User
from tailored_feed.services.session_student.session_student_get_service_interface import SessionStudentGetServiceInterface

class SessionStudentGetService(SessionStudentGetServiceInterface):
    
    def __init__(self, get_repository, session_get_repository, user_get_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository
        self.session_get_repository = session_get_repository
        self.user_get_repository = user_get_repository


    def by_session_n_user(self, session_id, student_id):
        try:
            session = self.session_get_repository.by_id(session_id)
            user = self.user_get_repository.by_id(student_id)
            return self.get_repository.by_session_n_user(session, user)


        except Exception as e:
            argspec = inspect.getfullargspec(self.by_session_n_user)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_session_n_user", parameters, str(e))