import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.user import User
from tailored_feed.repositories.user.user_get_repository_interface import UserGetRepositoryInterface

class UserGetRepository(UserGetRepositoryInterface):
    
    def __init__(self):
        self.exception_manager = ExceptionManager()


    def by_id(self, id: int):
        try:
            return User.objects.get(id=id)
        
        except Exception as e:
            argspec = inspect.getfullargspec(self.by_id)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "by_id", parameters, str(e))