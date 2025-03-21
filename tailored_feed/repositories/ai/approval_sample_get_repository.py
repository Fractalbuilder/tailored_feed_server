import inspect
from django.db.models import Q
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.repositories.ai.approval_sample_get_repository_interface import ApprovalSampleGetRepositoryInterface

class ApprovalSampleGetRepository(ApprovalSampleGetRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()
        
    
    def finished_session_students_answers(
        self, assessment_id, question_index_assessed, assessment_last_question_index
    ):
        try:
            return SessionAnswer.objects.filter(
                questionIndex__lte=question_index_assessed,
                sessionStudent__currentQuestionIndex=assessment_last_question_index,
                sessionStudent__session__assessment_id=assessment_id
            )

        except Exception as e:
            argspec = inspect.getfullargspec(self.finished_session_students_answers)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "finished_session_students_answers", parameters, str(e))

    
    def student_answers_from_index(
        self, session_student_id, question_index_assessed
    ):
        try:
            return SessionAnswer.objects.filter(
                questionIndex__lte=question_index_assessed,
                sessionStudent__id=session_student_id
            )

        except Exception as e:
            argspec = inspect.getfullargspec(self.student_answers_from_index)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "student_answers_from_index", parameters, str(e))
