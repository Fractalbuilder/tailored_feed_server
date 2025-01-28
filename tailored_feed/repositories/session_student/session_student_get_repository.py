import inspect
from django.db.models import Q
from django.utils.timezone import now
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.repositories.session_student.session_student_get_repository_interface import SessionStudentGetRepositoryInterface

class SessionStudentGetRepository(SessionStudentGetRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def by_session_n_user(self, session, user):
        try:
            """
            Fetch a SessionStudent by session and student.
            If it doesn't exist, create a new one.
            """
            session_student, created = SessionStudent.objects.get_or_create(
                session=session,
                student=user,
                defaults={
                    "creationDate": now(),
                    "approvedQuestions": 0,
                    "failedQuestions": 0,
                    "currentQuestionIndex": -1
                }
            )
            return session_student
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_session_n_user)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_session_n_user", parameters, str(e))