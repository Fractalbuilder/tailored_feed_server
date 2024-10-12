import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_remove_repository import AssessmentRemoveRepository
from tailored_feed.services.assessment.assessment_remove_service import AssessmentRemoveService

log_manager = LogManager()
assessment_remove_service = AssessmentRemoveService(AssessmentRemoveRepository())

class AssessmentRemoveController:

    @staticmethod
    def remove(request, assessment_id):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            assessment_remove_service.remove_n_save(assessment_id=assessment_id)
            messages.success(request, 'La evaluación se eliminó exitosamente')

        except ContentError as e:
            messages.error(request, "Eliminación fallida. " + str(e))

        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: remove())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')

        return redirect('assessment_dashboard')