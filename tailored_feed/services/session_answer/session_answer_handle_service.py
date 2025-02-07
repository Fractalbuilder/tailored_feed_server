import inspect
import numpy as np
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.services.session_answer.session_answer_handle_service_interface import SessionAnswerHandleServiceInterface

class SessionAnswerHandleService(SessionAnswerHandleServiceInterface):

    def __init__(
        self, session_get_service, user_get_service, session_student_add_service, 
        session_answer_add_service, question_get_service
    ):
        self.exception_manager = ExceptionManager()
        self.session_get_service = session_get_service
        self.user_get_service = user_get_service
        self.session_student_add_service = session_student_add_service
        self.session_answer_add_service = session_answer_add_service
        self.question_get_service = question_get_service


    def handle(
        self, question_id: int, selected_options, session_id: int, 
        student_id: int, current_question_index: int, userContext: dict
    ):
        try:
            is_correct = False
            session = self.session_get_service.by_id(session_id)
            student = self.user_get_service.by_id(student_id)
            question = self.question_get_service.by_index_and_assessment_id(
                current_question_index, session.assessment_id
            )
            correctAnswerIndices = question.options['correctAnswerIndices']

            if np.array_equal(selected_options, correctAnswerIndices):
                is_correct = True

            session_student = self.session_student_add_service.create_or_update_session_student(
                session, student, is_correct, current_question_index
            )

            session_answer = self.session_answer_add_service.add(
                question_id=question_id, 
                session_student=session_student, 
                selected_options=selected_options,
                userContext=userContext
            )

            return session_answer
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.handle)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "handle", parameters, str(e))