import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.question.question_remove_repository import QuestionRemoveRepository
from tailored_feed.services.question.question_remove_service import QuestionRemoveService

log_manager = LogManager()
question_remove_service = QuestionRemoveService(QuestionRemoveRepository())

class QuestionRemoveController:

    @staticmethod
    def remove(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            id = request.POST.get('id')
            assessment_id = request.POST.get('assessment_id')
            question_remove_service.remove_n_save(id=id)
            messages.success(request, 'La pregunta se eliminó exitosamente')

        except ContentError as e:
            messages.error(request, "Eliminación fallida. " + str(e))

        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: remove())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')

        return redirect('questions_view', assessment_id=assessment_id)