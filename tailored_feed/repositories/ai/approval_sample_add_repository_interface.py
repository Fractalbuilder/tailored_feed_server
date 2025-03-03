from abc import ABC, abstractmethod
from tailored_feed.models.ai.approval_sample import ApprovalSample

class ApprovalSampleAddRepositoryInterface(ABC):

    @abstractmethod
    def add(self, approval_sample: ApprovalSample):
        pass