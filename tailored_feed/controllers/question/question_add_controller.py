import inspect
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_add_repository import AssessmentAddRepository
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
from tailored_feed.services.assessment.assessment_add_service import AssessmentAddService
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.question.questions_arrange_service import QuestionsArrangeService
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_add_repository import QuestionAddRepository
from tailored_feed.services.question.question_add_service import QuestionAddService

log_manager = LogManager()
assessment_add_service = AssessmentAddService(AssessmentAddRepository())
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
questions_arrange_service = QuestionsArrangeService(QuestionGetRepository())
question_add_service = QuestionAddService(QuestionAddRepository(), questions_arrange_service, assessment_add_service)

class QuestionAddController:

    @staticmethod
    def view(request, assessment_id):
        try:
            context = {
                'assessment': {
                    'id': assessment_id
                }
            }
            return render(
                request, 'question/question_add.html',
                {'context': context}
            )
        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(QuestionAddController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            
            return redirect('error_page')
    
    
    @staticmethod
    def add(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = request.POST
            assessment_id = data.get('assessment_id')
            statement = data.get('statement')
            options = json.loads(data.get('options', '[]'))
            feedback_text = data.get('feedback_text', '')

            assessment = assessment_get_service.by_id(assessment_id)
            question = AssessmentQuestion(
                assessment=assessment,
                statement=statement,
                options=options,
                feedback_text=feedback_text,
                questionIndex=-1
            )
            
            question_add_service.add_n_save(question, assessment, request.FILES)

            messages.success(request, 'La pregunta se creó exitosamente')

        except ContentError as e:
            messages.error(request, "Creación fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(QuestionAddController.add)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return JsonResponse({'error': 'Se produjo un error. Contacte al administrador'}, status=500)

        return JsonResponse({'message': 'La pregunta se creó exitosamente'}, status=200)

