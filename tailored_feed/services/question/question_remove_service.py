import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.services.question.question_remove_service_interface import QuestionRemoveServiceInterface

class QuestionRemoveService(QuestionRemoveServiceInterface):
    def __init__(self, remove_repository):
        self.exception_manager = ExceptionManager()
        self.remove_repository = remove_repository


    def remove(self, id: int):
        try:
            self.remove_repository.remove(id=id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove", parametros, str(e))
    

    def remove_n_save(self, id: int):
        try:
            self.remove(id=id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.remove_n_save)
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "remove_n_save", parametros, str(e))