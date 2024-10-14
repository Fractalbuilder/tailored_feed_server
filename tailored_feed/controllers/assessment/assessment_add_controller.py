import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_add_repository import AssessmentAddRepository
from tailored_feed.services.assessment.assessment_add_service import AssessmentAddService

log_manager = LogManager()
assessment_add_service = AssessmentAddService(AssessmentAddRepository())

class AssessmentAddController:

    @staticmethod
    def add(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            name = request.POST.get('name')
            assessment_add_service.add_n_save(name=name, owner=request.user)
            messages.success(request, 'La evaluación se creó exitosamente')

        except ContentError as e:
            messages.error(request, "Creación fallida. " + str(e))

        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: add())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')

        return redirect('assessments_view')