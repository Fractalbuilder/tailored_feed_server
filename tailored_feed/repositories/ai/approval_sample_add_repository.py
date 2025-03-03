import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.ai.approval_sample import ApprovalSample

class ApprovalSampleAddRepository:

    def __init__(self):
        self.exception_manager = ExceptionManager()


    def add(self, approval_sample: ApprovalSample):
        try:
            approval_sample.save()

            return approval_sample

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))