from abc import ABC, abstractmethod

class QuestionRemoveRepositoryInterface(ABC):

    @abstractmethod
    def remove(self, id: int):
        pass