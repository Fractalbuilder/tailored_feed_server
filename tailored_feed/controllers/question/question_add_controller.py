import inspect, json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.question.question_get_service import QuestionGetService
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_add_repository import QuestionAddRepository
from tailored_feed.services.question.question_add_service import QuestionAddService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
question_get_service = QuestionGetService(QuestionGetRepository())
question_add_service = QuestionAddService(QuestionAddRepository())

class QuestionAddController:

    @staticmethod
    def question_add_view(request, assessment_id):
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
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: view())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')


    @staticmethod
    def add(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = json.loads(request.body)
            assessment_id = data.get('assessment_id')
            statement = data.get('statement')
            options = data.get('options', [])

            assessment = assessment_get_service.by_id(assessment_id)
            question = AssessmentQuestion(assessment=assessment, statement=statement, options=options)
            question_add_service.add_n_save(question)
            messages.success(request, 'La pregunta se creó exitosamente')

        except ContentError as e:
            messages.error(request, "Creación fallida. " + str(e))

        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: add())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return JsonResponse({'error':'Se produjo un error. Contacte al administrador'}, status=500)

        return JsonResponse({'message':'La pregunta se creó exitosamente'}, status=200)