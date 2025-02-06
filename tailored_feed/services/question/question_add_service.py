import inspect
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.services.question.question_add_service_interface import QuestionAddServiceInterface

class QuestionAddService(QuestionAddServiceInterface):

    def __init__(self, add_repository, arrange_service, assessment_add_service):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository
        self.arrange_service = arrange_service
        self.assessment_add_service = assessment_add_service


    def add(self, question: AssessmentQuestion):
        try:
            return self.add_repository.add(question)

        except Exception as e:
            argspec = inspect.getfullargspec(self.add)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add", parameters, str(e))
    
    
    def add_n_save(self, question: AssessmentQuestion, file):
        try:
            question = self.add(question)
            assessment = question.assessment
            
            if 'feedback_image' in file:
                feedback_image = file['feedback_image']
                ext = feedback_image.name.split('.')[-1]
                image_path = f'{assessment.id}/{question.id}.{ext}'
                question.feedback_image.save(image_path, feedback_image)

            self.arrange_service.arrange(assessment.id)
            assessment.totalQuestions = assessment.totalQuestions + 1
            self.assessment_add_service.add_n_save(assessment)
            
            return question.to_dict()
        
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.add_n_save)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "add_n_save", parameters, str(e))