from abc import ABC, abstractmethod

class QuestionsArrangeServiceInterface(ABC):

    @abstractmethod
    def arrange(self):
        pass