import inspect, json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
from tailored_feed.services.question.question_get_service import QuestionGetService
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.repositories.question.question_add_repository import QuestionAddRepository
from tailored_feed.services.question.question_add_service import QuestionAddService

log_manager = LogManager()
question_get_service = QuestionGetService(QuestionGetRepository())
question_add_service = QuestionAddService(QuestionAddRepository())

class QuestionUpdateController:

    @staticmethod
    def view(request, id: int):
        try:
            question = question_get_service.by_id(id)

            return render(
                request, 'question/question_update.html',
                {'question': question}
            )
            
        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(QuestionUpdateController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}

            return redirect('error_page')


    @staticmethod
    def update(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = request.POST
            id = data.get('id')
            statement = data.get('statement')
            options = json.loads(data.get('options', '[]'))
            feedback_text = data.get('feedback_text', '')

            question = question_get_service.by_id(id)
            question.statement = statement
            question.options = options
            question.feedback_text = feedback_text
            question.feedback_image = None

            if 'feedback_image' in request.FILES:
                feedback_image = request.FILES['feedback_image']
                ext = feedback_image.name.split('.')[-1]
                image_path = f'{question.assessment.id}/{id}.{ext}'
                question.feedback_image.save(image_path, feedback_image)

            question_add_service.add_n_save(question)
            messages.success(request, 'La pregunta se actualizó exitosamente')

        except ContentError as e:
            messages.error(request, "Actualización fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(QuestionUpdateController.update)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return JsonResponse({'error':'Se produjo un error. Contacte al administrador'}, status=500)

        return JsonResponse({'message':'La pregunta se actualizó exitosamente'}, status=200)