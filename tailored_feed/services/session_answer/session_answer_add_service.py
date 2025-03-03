import inspect
from django.utils.timezone import now
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.services.session_answer.session_answer_add_service_interface import SessionAnswerAddServiceInterface

class SessionAnswerAddService(SessionAnswerAddServiceInterface):

    def __init__(self, add_repository, question_get_service):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository
        self.question_get_service = question_get_service 


    def add(
        self, question_id: int, session_student, question_index, 
        selected_options, user_context, start_date, is_correct
    ):
        try:
            question = self.question_get_service.by_id(question_id)
            elapsed_time = int((now() - start_date).total_seconds() / 60)

            session_answer = SessionAnswer(
                assessmentQuestion=question,
                sessionStudent=session_student,
                questionIndex=question_index,
                selectedOptions=selected_options,
                userContext=user_context,
                elapsedTime=elapsed_time,
                isCorrect=is_correct
            )
            
            return self.add_repository.add(session_answer)
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))