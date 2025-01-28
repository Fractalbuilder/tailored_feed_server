import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.user import User
from tailored_feed.services.user.user_get_service_interface import UserGetServiceInterface

class UserGetService(UserGetServiceInterface):
    
    def __init__(self, get_repository):
        self.exception_manager = ExceptionManager()
        self.get_repository = get_repository


    def by_id(self, id):
        try:
            return self.get_repository.by_id(id)

        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parameters, str(e))