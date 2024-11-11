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
    def remove(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            id = request.POST.get('id')
            assessment_remove_service.remove_n_save(id=id)
            messages.success(request, 'La evaluación se eliminó exitosamente')

        except ContentError as e:
            messages.error(request, "Eliminación fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(AssessmentRemoveController.remove)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')

        return redirect('assessments_view')