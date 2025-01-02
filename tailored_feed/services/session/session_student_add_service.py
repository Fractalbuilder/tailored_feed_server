import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.models.session.session import Session
from tailored_feed.models.user import User
from tailored_feed.services.session.session_add_service_interface import SessionAddServiceInterface

class SessionAddService(SessionAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def add(self, session_id: int, student_id: int):
        try:
            session = Session.objects.get(id=session_id)

            if session is None:
                raise ContentError(f'No se encontró la sesión con ID {session_id}.')

            student = User.objects.get(id=student_id)

            if student is None:
                raise ContentError(f'No se encontró el estudiante con ID {student_id}.')

            if student.role != "student":
                raise ContentError(f'El usuario con ID {student_id} no es un estudiante.')

            session_student = SessionStudent(session=session, student=student)

            return self.add_repository.add(session_student=session_student)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))
    

    def add_n_save(self, session_id: int, student_id: int):
        try:
            session_student = self.add(session_id, student_id)
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parameters, str(e))