import inspect
from django.db.models import Q, Avg
from django.utils.timezone import now
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.repositories.session_student.session_student_get_repository_interface import SessionStudentGetRepositoryInterface

class SessionStudentGetRepository(SessionStudentGetRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def by_session(self, session):
        try:
            """
            Fetch SessionStudents by session.
            """
            return SessionStudent.objects.filter(session=session)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_session)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_session", parameters, str(e))

    
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
                    "correctAnswers": 0,
                    "wrongAnswers": 0,
                    "currentQuestionIndex": -1
                }
            )
            return session_student
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_session_n_user)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_session_n_user", parameters, str(e))


    def get_avg_question_index(self, session_id, last_question_index):
        try:
            average = SessionStudent.objects.filter(
                session_id=session_id
            ).exclude(
                currentQuestionIndex__in=[-1, last_question_index]
            ).aggregate(avg_question_index=Avg('currentQuestionIndex'))['avg_question_index']

            return int(average) if average is not None else 0

        except Exception as e:
            argspec = inspect.getfullargspec(self.get_avg_question_index)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "get_avg_question_index", parameters, str(e))
