import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.repositories.session_answer.session_answer_add_repository_interface import SessionAnswerAddRepositoryInterface

class SessionAnswerAddRepository(SessionAnswerAddRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def add(self, session_answer):
        try:
            session_answer.save()
            return session_answer

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))